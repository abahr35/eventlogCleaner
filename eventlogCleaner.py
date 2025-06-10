import re
import argparse
import csv
from datetime import datetime
import os


def extract_info(line):
    time = re.search(r'time="([^"]+)"', line)  # regex to find time
    src = re.search(r'src=([\d.]+)', line)     # regex to find source IP
    user = re.search(r'user="([^"]+)"', line)  # regex to find user
    country = re.search(r'geoCountryName="([^"]*)"', line)  # regex to find country

    if not (time and src and user):
        return None

    return {  # return a dictionary so i can easily sort
        "time": time.group(1),
        "ip": src.group(1),
        "user": user.group(1),
        "country": country.group(1) if country else 'Unknown'
    }


def process_log(input_path, output_path, sort_by=None, file_format='txt'):
    results = []

    with open(input_path, 'r') as infile:
        for line in infile:
            info = extract_info(line)
            if info:
                results.append(info)

    if sort_by:
        results.sort(key=lambda x: x.get(sort_by, ''))

    # Wire a new CSV file if selected
    if file_format == 'csv':
        with open(output_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Time", "IP", "User", "Country"])
            for entry in results:
                writer.writerow([entry['time'], entry['ip'], entry['user'], entry['country']])
    else:  # else Text
        with open(output_path, 'w') as outfile:
            for entry in results:
                outfile.write(f"{entry['time']} | {entry['ip']} | {entry['user']} | {entry['country']}\n")


if __name__ == '__main__':
    # Parser helps recognize arguments passed
    parser = argparse.ArgumentParser(description='Process and clean SSL VPN log files.')
    parser.add_argument('input_file', nargs='?', default='eventlog.txt', help='Input log file (default: eventlog.txt)')
    parser.add_argument('output_file', nargs='?', help='Output file name (default uses current date)')
    parser.add_argument('-s', '--sort', choices=['time', 'ip', 'country'],
                        help='Sort the output by this field: time, ip, or country')
    parser.add_argument('-f', '--format', choices=['txt', 'csv'], default='txt',
                        help='Output file format: txt or csv (default: txt)')

    args = parser.parse_args()
    date_suffix = datetime.now().strftime("%m%d%Y")  # add date for filename

    # set file extension based on format
    extension = args.format
    default_filename = f"cleaned_log_{date_suffix}.{extension}"

    output_file = args.output_file or default_filename  # use given filename or auto-generate one

    # If user-supplied output file doesn't match the format, correct it
    if not output_file.lower().endswith(f".{extension}"):
        output_file = os.path.splitext(output_file)[0] + f".{extension}"

    process_log(args.input_file, output_file, args.sort, args.format)
    print(f"Done. Cleaned log saved to '{output_file}'")
