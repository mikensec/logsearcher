import os
import argparse
import re
import json

def search_files(directory, search_terms):
    results = []

    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)

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
                        results.append({
                            "file": filepath,
                            "line_num": line_num,
                            "string": ' and '.join(combined_search),
                            "results": line.strip()
                        })

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

    results = search_files(args.directory, search_terms)

    if args.output:
        with open(args.output, 'w') as file:
            json.dump(results, file, indent=4)

    # Printing to console
    #for result in results:
    #    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
