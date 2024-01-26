"""The main script"""
import sys
import json
import logging

from selenium import webdriver

from uber_automation import UberAutomation

def getconfig() -> object:
    """Get the general configuration for the program."""
    with open('config/config.json', 'r') as config_file:
        config = json.load(config_file)

    return config

def configlogging(config: object) -> None:
    """Configure the logging."""
    handlers = [logging.FileHandler('log.log')]
    if config['verbose']: handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s|%(levelname)s|%(filename)s:%(message)s',
        handlers=handlers
    )


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
    config = getconfig()
    configlogging(config)

    logging.info("Running main program...")

    runbrowser()

    logging.info("Exiting program...")

    return 0

if __name__ == '__main__':
    sys.exit(run())
