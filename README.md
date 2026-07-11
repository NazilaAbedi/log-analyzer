# Log Analyzer CLI

A simple command-line tool for analyzing web server access logs.

The program reads access log files and creates a report about requests, IP addresses, status codes, errors, and traffic over time.

---

## How to Run


Run the program:

```bash
python3 main.py access.log
```

For JSON output:

```bash
python3 main.py access.log --json
```

The program also supports compressed log files:

```bash
python3 main.py access.log.gz
```

---

## Features

The program can:

- Count total requests
- Count unique IP addresses
- Calculate error rate
- Count 4xx and 5xx errors
- Show HTTP status code distribution
- Find the top 10 requested endpoints
- Show request count by hour
- Count invalid log lines

---

## Extra Features

### Suspicious IP Detection

The program finds IP addresses with many `401` responses.

This can help detect possible failed login attempts.

---

### Error Spike Detection

The program finds hours with a high rate of `5xx` errors.

---

### Gzip Support

The program can read `.gz` log files directly.
I'v used utility.py for this suuportation.

---

### JSON Output

The report can also be printed in JSON format.

---

## Project Structure

```
log-analyzer/
│
├── main.py          # Runs the program
├── parser.py        # Parses log lines
├── analyzer.py      # Calculates statistics
├── reporter.py      # Prints the report
├── utils.py         # Helper functions
├── tests/test1           # Test files
│
└── README.md
```

---

## Design Decisions

### Reading Logs

The log file is read line by line instead of loading the whole file into memory.

This helps the program work with large log files.

---

### Handling Bad Lines

Some log lines can be incomplete or broken.

The program skips these lines, counts them, and continues running.

---

### Libraries


This project uses only Python standard libraries, so no extra packages are needed.

Only Python standard libraries are used:

- `re`
- `datetime`
- `collections`
- `gzip`
- `json`
- `sys`

No external libraries are required.

---

## Challenges & Solutions

### 1. Empty Lines

**Problem:** The program was counting empty lines as bad lines.

**Solution:** Added a check for empty lines before parsing:

```python
line = line.strip()
if not line:
    return None
```

---

### 2. Size Field with "-" Value

**Problem:** Some log lines had `-` instead of a byte size. Converting `-` to int caused errors.

**Solution:** Check for `-` and replace it with `0`:

```python
if data["size"] == "-":
    data["size"] = 0
else:
    data["size"] = int(data["size"])
```

---

### 3. Git Ignore Issues

**Problem:** `access.log` and `__pycache__/` were accidentally added to Git.

**Solution:** Created a `.gitignore` file:

```
__pycache__/
*.pyc
*.log
*.gz
.DS_Store
```

Then removed the files from Git tracking:

```bash
git rm --cached access.log
git rm --cached -r __pycache__/
```

---

### 4. Testing with Real Log Files

**Problem:** The program was tested with clean sample files, but the real `access.log` file had many broken lines.

**Result:** The program handled almost 4,956 bad lines out of 495,044 total requests without crashing.

---

### 5. Gzip Testing

**Problem:** The program showed `File not found` when testing `.gz` files.

**Solution:** Created a compressed file with:

```bash
gzip -c access.log > access.log.gz
```

Then the program worked correctly.

---

## Key Learnings

1. Always create `.gitignore` before adding files to Git (i just wanna cry)
2. Real log files are not always clean
3. Always test with real data
4. Handle edge cases like empty lines and missing data

---

## Testing

The program was tested with:

- Large log files
- Broken log lines
- `.gz` compressed files
- Sample test files

The program can process logs without crashing.