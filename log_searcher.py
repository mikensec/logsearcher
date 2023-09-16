import os
import re
import sys
import json
from multiprocessing import Pool

def search_file(args):
    filepath, patterns = args
    results = []

    with open(filepath, 'r', errors='replace') as file:
        for lineno, line in enumerate(file, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    results.append({
                        "file": filepath,
                        "line": lineno,
                        "string": pattern,
                        "result": line.strip()
                    })
    return results

def main():
    if len(sys.argv) < 3:
        print("Usage: log_searcher.py <directory> <pattern1> [pattern2 ...] [--output output_file.json]")
        return

    directory = sys.argv[1]
    output_file = None

    # Extract patterns and check for --output flag
    patterns = []
    args = sys.argv[2:]
    while args:
        arg = args.pop(0)
        if arg == '--output' and args:
            output_file = args.pop(0)
        else:
            patterns.append(arg)

    if not patterns:
        print("At least one search pattern must be provided.")
        return

    # Convert combined queries using 'and' into single regex pattern
    for i, pattern in enumerate(patterns):
        if ' and ' in pattern:
            sub_patterns = pattern.split(' and ')
            combined_pattern = '(?=.*' + ')(?=.*'.join(map(re.escape, sub_patterns)) + ')'
            patterns[i] = combined_pattern

    all_files = [os.path.join(root, file) for root, dirs, files in os.walk(directory) for file in files]
    
    with Pool() as pool:
        results = pool.map(search_file, [(file, patterns) for file in all_files])
    results = [item for sublist in results for item in sublist]

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
    else:
        for entry in results:
            print(json.dumps(entry, indent=4))

if __name__ == "__main__":
    main()
