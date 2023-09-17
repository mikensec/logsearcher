import argparse
import os
import re
import json
import concurrent.futures

def search_files(directory, search_terms):
    results = []

    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            
            with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
                lines = file.readlines()
                for line_num, line in enumerate(lines):
                    if check_matching(line, search_terms):
                        result = {
                            "file": filepath,
                            "line_num": line_num + 1,
                            "string": " and ".join(search_terms).replace(" and or ", " or "),
                            "log": line.strip()
                        }
                        results.append(result)
                        
    return results

def check_matching(line, search_terms):
    or_groups = [group for group in ' '.join(search_terms).split(' or ')]

    for group in or_groups:
        terms = group.split(' and ')
        if all(re.search(term, line) for term in terms):
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Search for terms within logs in a given directory.")
    parser.add_argument("directory", type=str, help="The directory where the logs are stored.")
    parser.add_argument("search_terms", type=str, nargs='+', help="The terms to search for. Use 'and' or 'or' to specify multiple terms.")
    parser.add_argument("--output", type=str, default=None, help="Provide a filename to save the results in addition to printing them.")
    
    args = parser.parse_args()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.submit(search_files, args.directory, args.search_terms).result()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=4)
        print(json.dumps(results, indent=4))
    else:
        print(json.dumps(results, indent=4))
    
if __name__ == "__main__":
    main()
