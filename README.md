A simple Python script to parse, extract, and optionally sort data.
---
## Features:
- Extracts Key Info from the given log file  
  - Time of logged entry  
  - Source IP  
  - User  
- Supports output in .txt and .csv
- Supports sorting
- Auto-naming but supports custom naming

## How to run the cleaner
  - Ensure Python 3.11+ is install and added to PATH [Python download link](https://www.python.org/downloads/)
  - Open CMD and navigate to the root folder: example: ```cd C:\root```
  - Run the command ``` python eventlogCleaner.py  [options] [input_file] [output_file] ```
  - Example command to sort by time and create a csv: ``` python eventlogCleaner.py -s time -f csv eventlog.txt```

## Options
```
  -h, --help                                        Shows usage and options
  -s {time,ip,country}, --sort {time,ip,country}    Sort the output by this field: time, ip, or country
  -f {txt,csv}, --format {txt,csv}                  Output file format: txt or csv (default: txt)
```
