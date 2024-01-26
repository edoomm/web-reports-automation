"""The main script"""
import sys
import json
import logging
import argparse

from selenium import webdriver

from UberAutomation import UberAutomation

parser = argparse.ArgumentParser(description='Main script')

qh = 'Run the program quietly'
qa = 'store_true'
parser.add_argument('-q', '--quiet', action=qa, help=qh)

args = parser.parse_args()

def configlogging() -> None:
    """Configure the logging."""
    handlers = [logging.FileHandler('log.log')]
    if not args.quiet: handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s]|(%(levelname)s)|%(message)s',
        handlers=handlers
    )

def getconfig() -> object:
    """Get the general configuration for the program."""
    logging.info("Opening and getting configuration...")
    with open('config/config.json', 'r') as config_file:
        config = json.load(config_file)

    return config

def getbrowser() -> webdriver.chromium.webdriver.ChromiumDriver | webdriver.remote.webdriver.WebDriver:
    """Return the proper browser that will be used based on the
    configuration.
    """
    return webdriver.Firefox()

def runbrowser() -> None:
    """Run the browser where the work will be done.
    """
    logging.info("Starting browser...")
    browser = getbrowser()

    uber_automation = UberAutomation(browser)

    logging.info("Closing browser...")
    browser.close()

def run() -> int:
    """Run the main program."""
    configlogging()

    logging.info("Running main program...")

    config = getconfig()

    # runbrowser()

    logging.info("Exiting program...")

    return 0

if __name__ == '__main__':
    sys.exit(run())
