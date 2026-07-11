def print_report(stats):

    print("="*60)
    print("LOG ANALYSIS REPORT")
    print("="*60)


    print(
        f"Total Requests: {stats['total_requests']:,}"
    )

    print(
        f"Total Bytes: {stats['total_bytes']:,}"
    )

    print(
        f"Unique IPs: {stats['unique_ips']:,}"
    )

    print(
        f"Error Rate: {stats['error_rate']:.2f}%"
    )


    print(
        f"4xx Errors: {stats['4xx']}"
    )

    print(
        f"5xx Errors: {stats['5xx']}"
    )


    print(
        f"Bad Lines: {stats['bad_lines']}"
    )



    print("\nSTATUS CODES:")

    for code,count in stats["status_codes"].items():

        print(
            f"  {code}: {count}"
        )



    print("\nTOP 10 ENDPOINTS:")

    for i,(path,count) in enumerate(
        stats["top_endpoints"],
        1
    ):

        print(
            f"  {i}. {path}: {count}"
        )



    print("\nHOURLY DISTRIBUTION:")

    hourly = stats["hourly"]


    if hourly:

        maximum = max(
            hourly.values()
        )


        for hour,count in sorted(hourly.items()):

            bar = "#" * int(
                count / maximum * 50
            )

            print(
                f"  {hour} {bar} {count}"
            )



    if stats["suspicious_ips"]:

        print(
            "\nSUSPICIOUS IPS:"
        )


        for ip,data in stats["suspicious_ips"].items():

            print(
                f"  {ip}: "
                f"{data['401_count']} failures / "
                f"{data['requests']} requests "
                f"({data['failure_rate']:.1f}%)"
            )



    if stats["error_spikes"]:

        print(
            "\nERROR SPIKES:"
        )


        for item in stats["error_spikes"]:

            print(
                f"  {item['hour']}: "
                f"{item['rate']:.1f}% "
                f"({item['errors']}/{item['total']})"
            )