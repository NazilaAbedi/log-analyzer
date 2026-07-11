import sys
import json

from parser import parse_line
from analyzer import LogAnalyzer
from reporter import print_report
from utils import open_log_file


def main():

    if len(sys.argv) < 2 or len(sys.argv) > 3:

        print(
            "Usage: python3 main.py <log_file> [--json]"
        )

        sys.exit(1)


    file_path = sys.argv[1]

    json_output = False


    if len(sys.argv) == 3:

        if sys.argv[2] == "--json":
            json_output = True

        else:
            print(
                "Unknown option"
            )
            sys.exit(1)



    analyzer = LogAnalyzer()


    try:

        with open_log_file(file_path) as file:

            for line in file:

                data = parse_line(line)


                if data:

                    analyzer.process_line(data)

                else:

                    analyzer.add_bad_line()



    except FileNotFoundError:

        print(
            "File not found"
        )

        sys.exit(1)



    stats = analyzer.statistics()


    if json_output:

        print(
            json.dumps(
                convert_to_json(stats),
                indent=4
            )
        )

    else:

        print_report(stats)



def convert_to_json(data):

    result = {}


    for key, value in data.items():

        if hasattr(value, "items"):

            result[key] = dict(value)


        elif isinstance(value, list):

            result[key] = value


        else:

            result[key] = value


    return result



if __name__ == "__main__":
    main()