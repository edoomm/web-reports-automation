# web-reports-automation
Webscrapping through Uber and Edenred websites to download csv reports.

## Installation
```sh
git clone https://github.com/edoomm/web-reports-automation.git
cd web-reports-automation
pip install -r requirements.txt
```

## Usage
```sh
python src/run.py -h
usage: run.py [-h] [-i INTERACTIVE] [-w WEEK]

Download reports from uber and edenred automatically

options:
  -h, --help            show this help message and exit
  -i INTERACTIVE, --interactive INTERACTIVE
                        Run the program interactively
  -w WEEK, --week WEEK  Select and sets (in config) the number of the week for the report
```
