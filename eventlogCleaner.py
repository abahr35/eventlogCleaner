import re
import argparse
from datetime import datetime


def extract_info(line):
    time = re.search(r'time="([^"]+)"', line)  # regex to find time
    src = re.search(r'src=([\d.]+)', line)  # regex to find source IP
    user = re.search(r'user="([^"]+)"', line)  # regex to find user
    country = re.search(r'geoCountryName="([^"]*)"', line)  # regex for the country

    if not (time and src and user):  # Catch if data isn't there
        return None

    return {
        "time": time.group(1),
        "ip": src.group(1),
        "user": user.group(1),
        "country": country.group(1) if country else 'Unknown'
    }


def process_log(input_path, output_path, sort_by=None):
    results = []

    with open(input_path, 'r') as infile:
        for line in infile:
            info = extract_info(line)
            if info:
                results.append(info)

    if sort_by:
        results.sort(key=lambda x: x.get(sort_by, ''))

    with open(output_path, 'w') as outfile:
        for entry in results:
            outfile.write(f"{entry['time']} | {entry['ip']} | {entry['user']} | {entry['country']}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process and clean SSL VPN log files.')
    parser.add_argument('input_file', nargs='?', default='eventlog.txt', help='Input log file (default: eventlog.txt)')
    parser.add_argument('output_file', nargs='?', help='Output file name (default: cleaned_log_<MMDDYYYY>.txt)')
    parser.add_argument('-s', '--sort', choices=['time', 'ip', 'country'],
                        help='Sort the output by this field: time, ip, or country')

    args = parser.parse_args()

    # Generate date suffix
    date_suffix = datetime.now().strftime("%m%d%Y")

    # Use custom output file or build one with date
    output_file = args.output_file or f"cleaned_log_{date_suffix}.txt"

    process_log(args.input_file, output_file, args.sort)
    print(f"Done. Cleaned log saved to '{output_file}'")
    input("Press Enter to close...")
