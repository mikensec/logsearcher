import json
import sys

def generate_html_content(data):
    header = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Log Searcher Report</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #dddddd;
                padding: 8px;
                text-align: left;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>Log Searcher Report</h1>
        <table>
            <thead>
                <tr>
                    <th>File</th>
                    <th>Line Number</th>
                    <th>String Found</th>
                </tr>
            </thead>
            <tbody>
    """

    footer = """
            </tbody>
        </table>
    </body>
    </html>
    """

    rows = []
    for entry in data:
        row = f"""
        <tr>
            <td>{entry["file"]}</td>
            <td>{entry["line"]}</td>
            <td>{entry["string"]}</td>
        </tr>
        """
        rows.append(row)

    return header + "\n".join(rows) + footer

def generate_html_report(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    html_content = generate_html_content(data)

    with open(output_file, 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: json_to_html_report.py <input_json_file> <output_html_file>")
        sys.exit(1)

    input_json_file = sys.argv[1]
    output_html_file = sys.argv[2]

    generate_html_report(input_json_file, output_html_file)
    print(f"HTML report generated: {output_html_file}")
