def print_report(stats):

    print("=" * 60)
    print("LOG ANALYSIS REPORT")
    print("=" * 60)


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

    total = stats["total_requests"]


    for code, count in sorted(
        stats["status_codes"].items()
    ):

        bar = ""

        if total:
            bar = "#" * int(
                count / total * 40
            )


        print(
            f"  {code}: {count:>6} {bar}"
        )



    print("\nTOP ENDPOINTS:")

    for i, (endpoint, count) in enumerate(
        stats["top_endpoints"],
        1
    ):

        print(
            f"  {i}. {endpoint}: {count}"
        )



    print("\nHOURLY DISTRIBUTION:")

    hourly = stats["hourly"]


    if hourly:

        maximum = max(
            hourly.values()
        )


        for hour, count in sorted(
            hourly.items()
        ):

            bar = "#" * int(
                count / maximum * 50
            )


            print(
                f"  {hour} {bar} {count}"
            )



    suspicious = stats["suspicious_ips"]


    if suspicious:

        print(
            "\nSUSPICIOUS IPS:"
        )


        for ip, data in list(
            suspicious.items()
        )[:5]:

            print(
                f"  {ip}: "
                f"{data['401_count']} failures / "
                f"{data['total']} requests "
                f"({data['failure_rate']:.1f}%)"
            )



    spikes = stats["error_spikes"]


    if spikes:

        print(
            "\nERROR SPIKES:"
        )


        for spike in spikes[:3]:

            print(
                f"  {spike['hour']}: "
                f"{spike['error_rate']:.1f}% "
                f"({spike['errors']}/{spike['total']})"
            )