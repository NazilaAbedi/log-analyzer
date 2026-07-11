import sys
from parser import parse_line
from analyzer import LogAnalyzer

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <log_file_path>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    analyzer = LogAnalyzer()
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                parsed = parse_line(line)
                if parsed:
                    analyzer.process_line(parsed)
                else:
                    analyzer.bad_lines += 1
    except FileNotFoundError:
        print(f"Error: File '{log_file}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    print(analyzer.get_report())

if __name__ == "__main__":
    main()