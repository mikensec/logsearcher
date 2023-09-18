#!/usr/bin/env python3

import os
import argparse
import re
import json
import concurrent.futures

def search_file(filepath, search_terms):
    results = []

    with open(filepath, 'r', errors='replace') as file:
        for line_num, line in enumerate(file, 1):
            combined_search = []
            or_group_results = []

            # Evaluate OR groups first
            for or_group in search_terms:
                and_group_results = [re.search(term, line) for term in or_group]
                if all(and_group_results):
                    combined_search.extend(or_group)

            if combined_search:
                match_data = {
                    "file": filepath,
                    "line_num": line_num,
                    "string": ' and '.join(combined_search),
                    "results": line.strip()
                }
                results.append(match_data)

    return results

def main():
    parser = argparse.ArgumentParser(description="Search for strings in log files.")
    parser.add_argument("directory", help="Directory to search in.")
    parser.add_argument("search_terms", nargs="+", help="Search terms. Use 'and' & 'or' to combine.")
    parser.add_argument("--output", help="JSON output file name.")
    args = parser.parse_args()

    # Split search terms by 'or', then each group by 'and'
    raw_search_terms = ' '.join(args.search_terms).split(' or ')
    search_terms = [group.split(' and ') for group in raw_search_terms]

    all_results = []

    # Using a ThreadPool for concurrent file searching
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Using os.walk to generate a list of filepaths
        filepaths = [os.path.join(folder, filename) for folder, _, filenames in os.walk(args.directory) for filename in filenames]

        # Map filepaths to the search function, and collect results as they become available
        for result in executor.map(search_file, filepaths, [search_terms]*len(filepaths)):
            all_results.extend(result)

    if args.output:
        with open(args.output, 'w') as file:
            json.dump(all_results, file, indent=4)

    # Printing to console
    for result in all_results:
        print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
