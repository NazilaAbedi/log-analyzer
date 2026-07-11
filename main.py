import sys
from parser import parse_line
from analyzer import LogAnalyzer
from reporter import print_report

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <log_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    analyzer = LogAnalyzer()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parsed = parse_line(line)
                if parsed:
                    analyzer.process_line(parsed)
                else:
                    analyzer.add_bad_line()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    print_report(analyzer.get_statistics())

if __name__ == "__main__":
    main()