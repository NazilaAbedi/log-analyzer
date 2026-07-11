import re
from datetime import datetime


PATTERN = re.compile(
    r'(?P<ip>\S+) '
    r'\S+ \S+ '
    r'\[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) '
    r'(?P<path>\S+) '
    r'(?P<protocol>[^"]+)" '
    r'(?P<status>\d+) '
    r'(?P<size>\S+) '
    r'"(?P<referer>[^"]*)" '
    r'"(?P<user_agent>[^"]*)"'
)


def parse_line(line):

    try:
        match = PATTERN.match(line.strip())

        if not match:
            return None

        data = match.groupdict()

        data["status"] = int(data["status"])

        if data["size"] == "-":
            data["size"] = 0
        else:
            data["size"] = int(data["size"])


        data["time"] = datetime.strptime(
            data["time"],
            "%d/%b/%Y:%H:%M:%S %z"
        )

        return data


    except Exception:
        return None