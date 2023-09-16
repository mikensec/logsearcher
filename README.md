# Log Searcher by Michael Nieto @mikensec

## Description

Log Searcher is a Python script for searching through large log files for specific patterns using regular expressions. It's designed to be fast, using multi-threading to speed up the search process. The script also supports searching in subfolders and outputting the results in a JSON format.

## Requirements

- Python 3.x

No external libraries are required.

## Installation and Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/mikensec/logsearcher.git
   ```

2. Navigate to the folder containing the `log_searcher.py` file.

3. Make the script executable:

   **On Linux or macOS:**

   ```bash
   chmod +x log_searcher.py
   ```

   **On Windows:**
   No need to make it executable. Just run with Python.

4. Run the script:

   **On Linux or macOS:**

   ```bash
   ./log_searcher.py /path/to/logs "string1" "string2" --output my_results.json
   ```

   **On Windows:**

   ```powershell
   python log_searcher.py C:\path\to\logs "string1" "string2" --output my_results.json
   ```

## Search Patterns

- For a simple string search, just include the string in quotes: `"string"`
- To combine multiple search terms, use `and` (case-insensitive): `"string1" and "string2"`
- To search for multiple alternatives, use `or` (case-insensitive): `"string1" or "string2"`

If you provide terms without `and` or `or`, the script will search for each term individually across all log files.

## Examples

1. Search for IP addresses in the range 10.254.0.0/24:

   ```bash
   ./log_searcher.py /path/to/logs "^10\.254\.0\.([0-9]{1,2}|[01][0-9]{2}|2[0-4][0-9]|25[0-5])$"
   ```

2. Search for logs containing both `error` and `successful`:

   ```bash
   ./log_searcher.py /path/to/logs "error" and "successful"
   ```

3. Save search results to a file:
   ```bash
   ./log_searcher.py /path/to/logs "error" --output results.json
   ```

## Output

The output can be directed to both the terminal and a JSON file. Use the `--output` flag followed by the filename to specify the output file. When the `--output` flag is used, results are also printed on the terminal.
