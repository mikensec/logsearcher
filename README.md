# Log Searcher Tool By: Michael Nieto @mikensec

Created by Michael Nieto @mikensec

## Introduction

This script provides a fast and efficient way to search through large log directories for specific patterns. It uses regular expressions, multi-threading, and can output results in a JSON format.

## Requirements

- Python 3.x
- No external libraries are needed.

## Download

```bash
git clone https://github.com/mikensec/logsearcher.git
```

## Usage

### Making the script executable:

**Bash**:

```bash
chmod +x log_searcher.py
```

**Running the script**:

**Bash**:

```bash
./log_searcher.py /path/to/logs 'search_pattern1' 'search_pattern2' --output output_file.json
```

**PowerShell**:

```powershell
python .\log_searcher.py 'C:\path\to\logs' 'search_pattern1' 'search_pattern2' --output output_file.json
```

### Search Patterns:

You can provide multiple search patterns, and the script will search for logs containing any of the patterns.

#### Combined Query:

To search for logs containing multiple strings within the same line, use the `and` keyword:

```bash
./log_searcher.py /path/to/logs 'string1 and string2'
```

This will find lines containing both `string1` and `string2`.

#### Separate String and Regex Queries:

```bash
./log_searcher.py /path/to/logs 'string1' '^regex_pattern$'
```

This will find lines containing `string1` or matching the regex pattern.

### Example: Searching for IP Addresses

To search for all IP addresses in the range 10.254.0.0/24:

```bash
./log_searcher.py /path/to/logs '^10\.254\.0\.([0-9]{1,2}|[01][0-9]{2}|2[0-4][0-9]|25[0-5])$'
```

### Output:

If you want to save the results to a file, use the `--output` flag followed by the filename:

```bash
./log_searcher.py /path/to/logs 'search_pattern' --output results.json
```

If no `--output` flag is provided, the script will print results to the screen.

## Conclusion

This tool is designed to be a versatile and efficient solution for log searching tasks. Adapt the search patterns according to your needs and benefit from its speed and multi-threading capabilities.
