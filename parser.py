import re
from datetime import datetime
from typing import Optional, Dict


LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) - - '
    r'\[(?P<time>.*?)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>.*?)" '
    r'(?P<status>\d{3}) '
    r'(?P<size>\S+) '
    r'"(?P<referer>.*?)" '
    r'"(?P<user_agent>.*?)"$'
)


def parse_line(line: str) -> Optional[Dict]:

    match = LOG_PATTERN.match(line.strip())

    if not match:
        return None

    try:
        return {

            "ip": match.group("ip"),

            "time": datetime.strptime(
                match.group("time"),
                "%d/%b/%Y:%H:%M:%S %z"
            ),

            "method": match.group("method"),

            "path": match.group("path"),

            "protocol": match.group("protocol"),

            "status": int(match.group("status")),

            "size": (
                0
                if match.group("size") == "-"
                else int(match.group("size"))
            ),

            "referer": match.group("referer"),

            "user_agent": match.group("user_agent")
        }

    except Exception:
        return None