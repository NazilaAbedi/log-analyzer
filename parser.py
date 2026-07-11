import re
from datetime import datetime
from typing import Optional, Dict

LOG_PATTERN = re.compile(
    r'^(\S+) - - \[(.*?)\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+|-) "(.*?)" "(.*?)"$'
)

def parse_line(line: str) -> Optional[Dict]:
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    
    try:
        return {
            'ip': match.group(1),
            'time': datetime.strptime(match.group(2), '%d/%b/%Y:%H:%M:%S %z'),
            'method': match.group(3),
            'path': match.group(4),
            'protocol': match.group(5),
            'status': int(match.group(6)),
            'size': int(match.group(7)) if match.group(7) != '-' else 0,
            'referer': match.group(8),
            'user_agent': match.group(9)
        }
    except Exception:
        return None