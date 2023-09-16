#Log Searcher by: Michael Nieto @mikensec
import os
import re
import json
import argparse
from multiprocessing import Pool

def search_file(args):
    filepath, patterns = args
    results = []

    with open(filepath, 'r', errors='replace') as file:
        for line_num, line in enumerate(file, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    results.append({
                        "file": filepath,
                        "line": line_num,
                        "string": pattern,
                        "result": line.strip()
                    })

    return results

def process_logs(directory_path, patterns):
    all_files = []

    for dirpath, _, filenames in os.walk(directory_path):
        for filename in filenames:
            all_files.append(os.path.join(dirpath, filename))

    with Pool() as pool:
        all_results = pool.map(search_file, [(f, patterns) for f in all_files])

    # Flatten the list of lists
    results = [item for sublist in all_results for item in sublist]

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search logs using regex patterns.")
    parser.add_argument("directory", help="Directory containing the log files.")
    parser.add_argument("search_terms", nargs='+', help="Patterns to search for. Use 'and' between patterns to search for combined queries. Use spaces between distinct queries.")
    parser.add_argument("--output", help="Output file to save the results in JSON format. If not specified, results will be printed on screen.")
    
    args = parser.parse_args()

    # Split search terms at spaces, treating 'and' as a combined search
    patterns = [term for term in args.search_terms if term.lower() != 'and']

    results = process_logs(args.directory, patterns)

    # If an output file is specified, write to that file
    if args.output:
        with open(args.output, 'w') as outfile:
            json.dump(results, outfile, indent=4)
        print(f"Results saved to {args.output}.")

    # Always print results to screen
    print(json.dumps(results, indent=4))
