from collections import Counter, defaultdict


class LogAnalyzer:


    def __init__(self):

        self.total_requests = 0
        self.total_bytes = 0

        self.unique_ips = set()

        self.endpoints = Counter()
        self.status_codes = Counter()

        self.hourly_requests = defaultdict(int)
        self.hourly_5xx = defaultdict(int)

        self.ip_status = defaultdict(
            lambda: defaultdict(int)
        )


        self.error_4xx = 0
        self.error_5xx = 0

        self.bad_lines = 0



    def process_line(self, data):

        self.total_requests += 1

        self.total_bytes += data["size"]

        self.unique_ips.add(
            data["ip"]
        )

        self.endpoints[
            data["path"]
        ] += 1


        status = data["status"]

        self.status_codes[status] += 1


        self.ip_status[
            data["ip"]
        ][status] += 1



        hour = data["time"].strftime(
            "%Y-%m-%d %H:00"
        )


        self.hourly_requests[hour] += 1



        if 400 <= status < 500:

            self.error_4xx += 1


        elif 500 <= status < 600:

            self.error_5xx += 1

            self.hourly_5xx[hour] += 1



    def add_bad_line(self):

        self.bad_lines += 1




    def suspicious_ips(self):

        result = {}


        for ip, statuses in self.ip_status.items():

            total = sum(
                statuses.values()
            )

            failed = statuses.get(
                401,
                0
            )


            if total >= 5:

                rate = failed / total


                if rate > 0.5:

                    result[ip] = {

                        "requests": total,

                        "401_count": failed,

                        "failure_rate": rate * 100

                    }


        return result




    def error_spikes(self, threshold=10):

        result = []


        for hour,total in self.hourly_requests.items():

            errors = self.hourly_5xx.get(
                hour,
                0
            )


            rate = (
                errors / total
            ) * 100


            if rate > threshold:

                result.append({

                    "hour": hour,

                    "errors": errors,

                    "total": total,

                    "rate": rate

                })


        return sorted(
            result,
            key=lambda x:x["rate"],
            reverse=True
        )




    def statistics(self):

        errors = (
            self.error_4xx +
            self.error_5xx
        )


        error_rate = 0


        if self.total_requests:

            error_rate = (
                errors /
                self.total_requests
            ) * 100



        return {

            "total_requests":
                self.total_requests,


            "total_bytes":
                self.total_bytes,


            "unique_ips":
                len(self.unique_ips),


            "error_rate":
                error_rate,


            "4xx":
                self.error_4xx,


            "5xx":
                self.error_5xx,


            "status_codes":
                self.status_codes,


            "top_endpoints":
                self.endpoints.most_common(10),


            "hourly":
                self.hourly_requests,


            "bad_lines":
                self.bad_lines,


            "suspicious_ips":
                self.suspicious_ips(),


            "error_spikes":
                self.error_spikes()

        }