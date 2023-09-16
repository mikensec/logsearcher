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
                    all_present = all(re.search(term, line) for term in search_terms if term not in ['and', 'or'])
                    if all_present:
                        result = {
                            "file": filepath,
                            "line_num": line_num + 1,
                            "string": " and ".join(search_terms),
                            "log": line.strip()
                        }
                        results.append(result)
                        
    return results

def main():
    parser = argparse.ArgumentParser(description="Search for terms within logs in a given directory.")
    parser.add_argument("directory", type=str, help="The directory where the logs are stored.")
    parser.add_argument("search_terms", type=str, nargs='+', help="The terms to search for. Use 'and' or 'or' to specify multiple terms.")
    parser.add_argument("--output", type=str, default=None, help="Provide a filename to save the results in addition to printing them.")
    
    args = parser.parse_args()
    
    search_terms = args.search_terms
    combined_search_terms = []
    
    tmp_terms = []
    for term in search_terms:
        term = term.lower()
        if term == "and":
            combined_search_terms.append(tmp_terms)
            tmp_terms = []
        else:
            tmp_terms.append(term)
    combined_search_terms.append(tmp_terms)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        all_results = []
        for search_set in combined_search_terms:
            all_results.extend(executor.submit(search_files, args.directory, search_set).result())
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(all_results, f, indent=4)
        print(json.dumps(all_results, indent=4))
    else:
        print(json.dumps(all_results, indent=4))
    
if __name__ == "__main__":
    main()
