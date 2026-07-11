from collections import Counter, defaultdict
from typing import Dict

class LogAnalyzer:
    def __init__(self):
        self.total_requests = 0
        self.total_bytes = 0
        self.unique_ips = set()
        self.endpoints = Counter()
        self.status_codes = Counter()
        self.user_agents = Counter()  # اضافه شده
        self.hourly_requests = defaultdict(int)
        self.error_4xx = 0
        self.error_5xx = 0
        self.bad_lines = 0
    
    def process_line(self, data: Dict):
        """Process a parsed log line"""
        self.total_requests += 1
        self.total_bytes += data["size"]
        
        self.unique_ips.add(data["ip"])
        self.endpoints[data["path"]] += 1
        self.user_agents[data["user_agent"]] += 1
        
        status = data["status"]
        self.status_codes[status] += 1
        
        if 400 <= status < 500:
            self.error_4xx += 1
        elif 500 <= status < 600:
            self.error_5xx += 1
        
        hour = data["time"].strftime("%Y-%m-%d %H:00")
        self.hourly_requests[hour] += 1
    
    def add_bad_line(self):
        """Increment bad lines counter"""
        self.bad_lines += 1
    
    def get_statistics(self) -> Dict:
        """Return all statistics as a dictionary"""
        errors = self.error_4xx + self.error_5xx
        error_rate = (errors / self.total_requests * 100) if self.total_requests > 0 else 0
        
        return {
            "total_requests": self.total_requests,
            "total_bytes": self.total_bytes,
            "unique_ips": len(self.unique_ips),
            "error_rate": error_rate,
            "4xx": self.error_4xx,
            "5xx": self.error_5xx,
            "status_codes": self.status_codes,
            "top_endpoints": self.endpoints.most_common(10),
            "top_user_agents": self.user_agents.most_common(5),  # اضافه شده
            "hourly": self.hourly_requests,
            "bad_lines": self.bad_lines
        }