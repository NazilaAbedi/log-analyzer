from collections import Counter, defaultdict
from typing import Dict


class LogAnalyzer:

    def __init__(self):

        self.total_requests = 0

        self.total_bytes = 0

        self.unique_ips = set()

        self.endpoints = Counter()

        self.status_codes = Counter()

        self.hourly_requests = defaultdict(int)

        self.hourly_errors = defaultdict(int)

        self.ip_status_counts = defaultdict(
            lambda: defaultdict(int)
        )

        self.error_4xx = 0

        self.error_5xx = 0

        self.bad_lines = 0



    def process_line(self, data: Dict):

        self.total_requests += 1

        self.total_bytes += data["size"]


        self.unique_ips.add(
            data["ip"]
        )


        self.endpoints[
            data["path"]
        ] += 1


        status = data["status"]


        self.status_codes[
            status
        ] += 1


        self.ip_status_counts[
            data["ip"]
        ][status] += 1



        hour = data["time"].strftime(
            "%Y-%m-%d %H:00"
        )


        self.hourly_requests[
            hour
        ] += 1



        if 400 <= status < 500:

            self.error_4xx += 1


        elif 500 <= status < 600:

            self.error_5xx += 1

            self.hourly_errors[
                hour
            ] += 1



    def add_bad_line(self):

        self.bad_lines += 1



    def get_suspicious_ips(
        self,
        threshold=0.5,
        min_requests=5
    ):

        suspicious = {}


        for ip, statuses in self.ip_status_counts.items():

            total = sum(
                statuses.values()
            )


            failures = statuses.get(
                401,
                0
            )


            if total >= min_requests:

                rate = failures / total


                if rate > threshold:

                    suspicious[ip] = {

                        "total": total,

                        "401_count": failures,

                        "failure_rate":
                            rate * 100
                    }


        return suspicious



    def get_error_spikes(
        self,
        threshold=10
    ):

        spikes = []


        for hour in self.hourly_requests:

            total = self.hourly_requests[hour]

            errors = self.hourly_errors.get(
                hour,
                0
            )


            if total > 0:

                rate = (
                    errors /
                    total
                ) * 100


                if rate > threshold:

                    spikes.append({

                        "hour": hour,

                        "error_rate": rate,

                        "errors": errors,

                        "total": total

                    })


        return sorted(
            spikes,
            key=lambda x: x["error_rate"],
            reverse=True
        )



    def get_statistics(self):

        errors = (
            self.error_4xx +
            self.error_5xx
        )


        error_rate = (

            errors /
            self.total_requests *
            100

            if self.total_requests
            else 0
        )


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
                dict(self.status_codes),

            "top_endpoints":
                self.endpoints.most_common(10),

            "hourly":
                dict(self.hourly_requests),

            "bad_lines":
                self.bad_lines,

            "suspicious_ips":
                self.get_suspicious_ips(),

            "error_spikes":
                self.get_error_spikes()
        }