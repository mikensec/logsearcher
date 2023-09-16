import os
import re
import json
import argparse
import multiprocessing

def search_file(args):
    filepath, patterns = args
    results = []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for lineno, line in enumerate(f, 1):
            all_found = all(any(re.search(pattern, line) for pattern in or_group) for or_group in patterns)
            if all_found:
                results.append((filepath, lineno, line.strip(), patterns))

    return results

def parse_search_terms(terms):
    and_groups = [group.split(' or ') for group in terms]
    and_groups = [[term.strip().lower() for term in group] for group in and_groups]

    return and_groups

def main():
    parser = argparse.ArgumentParser(description='Search log files for patterns.')
    parser.add_argument('directory', help='Directory containing log files.')
    parser.add_argument('search_terms', nargs='+', help='Terms to search for. Use "and" for AND operations, "or" for OR operations.')
    parser.add_argument('--output', help='Output to a JSON file.', action='store_true')

    args = parser.parse_args()

    search_terms = parse_search_terms(args.search_terms)

    pool = multiprocessing.Pool()
    files = [os.path.join(root, file) for root, dirs, files in os.walk(args.directory) for file in files]

    results = []
    for file_results in pool.imap(search_file, [(f, search_terms) for f in files]):
        results.extend(file_results)

    output = {
        "search": args.search_terms,
        "results": [
            {
                "file": r[0],
                "line": r[1],
                "match": r[2],
                "log": r[3]
            } for r in results
        ]
    }

    if args.output:
        with open('output.json', 'w') as f:
            json.dump(output, f, indent=4)

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()
