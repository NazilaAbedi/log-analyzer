from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Tuple

class LogAnalyzer:
    def __init__(self):
        self.total_requests = 0
        self.unique_ips = set()
        self.endpoints = Counter()
        self.error_4xx = 0
        self.error_5xx = 0
        self.hourly_counts = defaultdict(int)
        self.bad_lines = 0
    
    def process_line(self, parsed: Dict):
        self.total_requests += 1
        self.unique_ips.add(parsed['ip'])
        self.endpoints[parsed['path']] += 1
        
        hour = parsed['time'].strftime('%Y-%m-%d %H:00')
        self.hourly_counts[hour] += 1
        
        status = parsed['status']
        if 400 <= status < 500:
            self.error_4xx += 1
        elif 500 <= status < 600:
            self.error_5xx += 1
    
    def get_report(self) -> str:
        total_errors = self.error_4xx + self.error_5xx
        error_rate = (total_errors / self.total_requests * 100) if self.total_requests > 0 else 0
        
        top_endpoints = self.endpoints.most_common(10)
        
        hours = sorted(self.hourly_counts.keys())
        max_count = max(self.hourly_counts.values()) if hours else 1
        
        report = []
        report.append("="*60)
        report.append("LOG ANALYSIS REPORT")
        report.append("="*60)
        report.append(f"Total Requests: {self.total_requests:,}")
        report.append(f"Unique IPs: {len(self.unique_ips):,}")
        report.append(f"Error Rate (4xx + 5xx): {error_rate:.2f}%")
        report.append(f"  - 4xx Errors: {self.error_4xx}")
        report.append(f"  - 5xx Errors: {self.error_5xx}")
        report.append(f"Bad Lines: {self.bad_lines}")
        
        report.append("\nTOP 10 ENDPOINTS:")
        for i, (endpoint, count) in enumerate(top_endpoints, 1):
            report.append(f"  {i:2d}. {endpoint}: {count}")
        
        report.append("\nHOURLY DISTRIBUTION:")
        for hour in hours:
            count = self.hourly_counts[hour]
            bar = "█" * int((count / max_count) * 50)
            report.append(f"  {hour}  {bar} {count}")
        
        return "\n".join(report)