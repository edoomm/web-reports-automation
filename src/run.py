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

def getfirefox(path: str) -> webdriver.remote.webdriver.WebDriver:
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.profile = path

    return webdriver.Firefox(options=firefox_options)

def getbrowser(
        config: object
    ) -> webdriver.chromium.webdriver.ChromiumDriver | webdriver.remote.webdriver.WebDriver:
    """Return the proper browser that will be used based on the
    configuration.
    """
    if config['default_browser'] == "firefox":
        return getfirefox(config['firefox_profile_path'])

    return webdriver.Firefox()

def runbrowser(config: object) -> None:
    """Run the browser where the work will be done.
    """
    logging.info("Starting browser...")
    browser = getbrowser(config)

    uber_automation = UberAutomation(browser)

    input("PRESS [ENTER] TO CLOSE BROWSER... ")

    logging.info("Closing browser...")
    browser.close()

def run() -> int:
    """Run the main program."""
    config = getconfig()
    configlogging(config)

    logging.info("Running main program...")

    runbrowser(config)

    logging.info("Exiting program...")

    return 0

if __name__ == '__main__':
    sys.exit(run())
