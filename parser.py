import re
from datetime import datetime
from typing import Optional, Dict

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) .* \[(?P<time>.*?)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>.*?)" '
    r'(?P<status>\d{3}) (?P<size>\S+)'
)

def parse_line(line: str) -> Optional[Dict]:
    """Parse a single log line in Combined Log Format"""
    if not line or not line.strip():
        return None
    
    match = LOG_PATTERN.search(line)
    if not match:
        return None
    
    try:
        return {
            'ip': match.group('ip'),
            'time': datetime.strptime(match.group('time'), '%d/%b/%Y:%H:%M:%S %z'),
            'method': match.group('method'),
            'path': match.group('path'),
            'protocol': match.group('protocol'),
            'status': int(match.group('status')),
            'size': int(match.group('size')) if match.group('size') != '-' else 0
        }
    except (ValueError, KeyError):
        return None