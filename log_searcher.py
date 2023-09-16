import os
import re
import json
import argparse
from multiprocessing import Pool

def search_file(args):
    filepath, combined_patterns = args
    results = []

    with open(filepath, 'r', errors='replace') as file:
        for line_num, line in enumerate(file, 1):
            for pattern, search_string in combined_patterns:
                if all(re.search(p, line) for p in pattern):
                    results.append({
                        "file": filepath,
                        "line": line_num,
                        "string": search_string,
                        "result": line.strip()
                    })

    return results

def process_logs(directory_path, combined_patterns):
    all_files = []

    for dirpath, _, filenames in os.walk(directory_path):
        for filename in filenames:
            all_files.append(os.path.join(dirpath, filename))

    with Pool() as pool:
        all_results = pool.map(search_file, [(f, combined_patterns) for f in all_files])

    # Flatten the list of lists
    results = [item for sublist in all_results for item in sublist]

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search logs using regex patterns.")
    parser.add_argument("directory", help="Directory containing the log files.")
    parser.add_argument("search_terms", nargs='+', help="Patterns to search for. Use 'and' between patterns to search for combined queries. Use spaces between distinct queries.")
    parser.add_argument("--output", help="Output file to save the results in JSON format. If not specified, results will be printed on screen.")
    
    args = parser.parse_args()

    # Grouping search terms
    combined_patterns = []
    temp_patterns = []
    search_string = ""

    for term in args.search_terms:
        if term.lower() == 'and':
            search_string += " and "
        else:
            temp_patterns.append(term)
            search_string += term
            if len(temp_patterns) > 1:
                combined_patterns.append((temp_patterns, search_string))
                temp_patterns = []
                search_string = ""
            else:
                combined_patterns.append((temp_patterns, search_string))

    results = process_logs(args.directory, combined_patterns)

    # If an output file is specified, write to that file
    if args.output:
        with open(args.output, 'w') as outfile:
            json.dump(results, outfile, indent=4)
        print(f"Results saved to {args.output}.")

    # Always print results to screen
    print(json.dumps(results, indent=4))
