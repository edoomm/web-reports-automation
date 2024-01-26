"""The main script"""
import sys
import json
import logging

from selenium import webdriver

from uber_automation import UberAutomation

def getconfig() -> None:
    """Get the general configuration for the program."""
    global config

    with open('config/config.json', 'r') as config_file:
        config = json.load(config_file)

def configlogging() -> None:
    """Configure the logging."""
    global config

    handlers = [logging.FileHandler('log.log')]
    if config['verbose']: handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s|%(levelname)s|%(filename)s:%(message)s',
        handlers=handlers
    )

def getfirefox(path: str) -> webdriver.remote.webdriver.WebDriver:
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.profile = path

    return webdriver.Firefox(options=firefox_options)

def getbrowser() -> webdriver.chromium.webdriver.ChromiumDriver | webdriver.remote.webdriver.WebDriver:
    """Return the proper browser that will be used based on the
    configuration.
    """
    global config

    if config['default_browser'] == "firefox":
        return getfirefox(config['firefox_profile_path'])

    return webdriver.Firefox()

def runbrowser() -> None:
    """Run the browser where the work will be done.
    """
    global config

    logging.info("Starting browser...")
    browser = getbrowser()

    uber_automation = UberAutomation(browser)

    input("PRESS [ENTER] TO CLOSE BROWSER... ")

    logging.info("Closing browser...")
    browser.close()

def run() -> int:
    """Run the main program."""
    try:
        getconfig()
        configlogging()

        logging.info("Running main program...")

        runbrowser()

        logging.info("Exiting program succesfully...")

        return 0
    except json.decoder.JSONDecodeError as jde:
        logging.error(jde)

        msg = 'Cannot read config.json, make sure it follows a JSON structure'
        logging.error(msg)

        return 1
    except FileNotFoundError as fnfe:
        logging.error(fnfe)

        msg = 'Make sure to have correctly set file names in config.json'
        logging.error(msg)

        return 2

if __name__ == '__main__':
    sys.exit(run())
