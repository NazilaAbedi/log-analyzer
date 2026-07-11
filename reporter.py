def print_report(stats: dict):
    """Print formatted report"""
    print("=" * 60)
    print("LOG ANALYSIS REPORT")
    print("=" * 60)
    
    print(f"Total Requests: {stats['total_requests']:,}")
    print(f"Total Bytes Transferred: {stats['total_bytes']:,}")
    print(f"Unique IPs: {stats['unique_ips']:,}")
    print(f"Error Rate: {stats['error_rate']:.2f}%")
    print(f"  4xx Errors: {stats['4xx']}")
    print(f"  5xx Errors: {stats['5xx']}")
    print(f"Bad Lines: {stats['bad_lines']}")
    
    print("\nSTATUS CODE DISTRIBUTION:")
    for code, count in stats["status_codes"].most_common():
        bar = "#" * int((count / stats['total_requests']) * 40) if stats['total_requests'] > 0 else ""
        print(f"  {code}: {count:>6} {bar}")
    
    print("\nTOP 10 ENDPOINTS:")
    for i, (endpoint, count) in enumerate(stats["top_endpoints"], 1):
        print(f"  {i:2d}. {endpoint}: {count}")
    
    print("\nTOP 5 USER AGENTS:")
    for i, (agent, count) in enumerate(stats["top_user_agents"], 1):
        # Shorten long user agents
        if len(agent) > 50:
            agent = agent[:47] + "..."
        print(f"  {i}. {agent}: {count}")
    
    print("\nHOURLY DISTRIBUTION:")
    hourly = stats["hourly"]
    if hourly:
        max_count = max(hourly.values())
        for hour, count in sorted(hourly.items()):
            bar = "#" * int((count / max_count) * 50)
            print(f"  {hour}  {bar} {count}")