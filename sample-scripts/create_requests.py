# bin/python

import csv
import sys
import json
def parse_csv(file_name):
    try:
        with open(file_name) as file:
            csv_reader = csv.reader(file)
            rows = [row for row in csv_reader][1:]
            for row in rows:
                app = row[2]
                permission = row[3]
                user = row[4]
                reason = json.loads(row[6]).get("PENDING")
                print(f"lumos request --app-like '{app}' --permission-like '{permission}' --user-like {user} --reason \"{reason}\"")
    except FileNotFoundError:
        print("File not found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_requests.py <file_name>")
    else:
        file_name = sys.argv[1]
        parse_csv(file_name)