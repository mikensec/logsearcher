#!/usr/bin/env python3

import os
import argparse
import re
import json
import concurrent.futures
import sys

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

def display_progress_bar(iteration, total, bar_length=50):
    progress = (iteration / total)
    arrow = '=' * int(round(progress * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    
    sys.stdout.write(f'\rProgress: [{arrow + spaces}] {int(progress * 100)}%')
    sys.stdout.flush()

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

    # Using os.walk to generate a list of filepaths
    filepaths = [os.path.join(folder, filename) for folder, _, filenames in os.walk(args.directory) for filename in filenames]

    # Using a ThreadPool for concurrent file searching
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_filepath = {executor.submit(search_file, filepath, search_terms): filepath for filepath in filepaths}
        for index, future in enumerate(concurrent.futures.as_completed(future_to_filepath)):
            result = future.result()
            all_results.extend(result)
            display_progress_bar(index + 1, len(filepaths))
    
    print()  # Add a newline after the progress bar

    if args.output:
        with open(args.output, 'w') as file:
            json.dump(all_results, file, indent=4)

    # Printing to console
    for result in all_results:
        print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
