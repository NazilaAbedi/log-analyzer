import sys
import json

from parser import parse_line
from analyzer import LogAnalyzer
from reporter import print_report
from utils import open_log_file



def convert_json(data):

    result = {}


    for key,value in data.items():

        if hasattr(value,"items"):

            result[key] = dict(value)


        elif isinstance(value,list):

            result[key] = value


        else:

            result[key] = value


    return result




def main():

    if len(sys.argv) < 2:

        print(
            "Usage: python3 main.py <log_file> [--json]"
        )

        return



    file_path = sys.argv[1]


    json_output = (
        len(sys.argv) == 3
        and sys.argv[2]=="--json"
    )


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

        print("File not found")

        return



    stats = analyzer.statistics()



    if json_output:

        print(
            json.dumps(
                convert_json(stats),
                indent=4,
                default=str
            )
        )


    else:

        print_report(stats)




if __name__=="__main__":

    main()