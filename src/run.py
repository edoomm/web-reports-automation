"""The main script"""
import sys
import json
import logging

from selenium import webdriver

from uber_automation import UberAutomation
from edenred_automation import EdenredAutomation

def set_config() -> None:
    """Get the general configuration for the program."""
    global config

    with open('config/config.json', 'r') as config_file:
        config = json.load(config_file)

def config_logging() -> None:
    """Configure the logging."""
    global config

    handlers = [logging.FileHandler('log.log')]
    if config['verbose']: handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s|%(levelname)s|%(filename)s:%(message)s',
        handlers=handlers
    )

def get_firefox(path: str) -> webdriver.remote.webdriver.WebDriver:
    """Get the default firefox browser for the current system."""
    logging.info("Creating firefox browser...")

    firefox_options = webdriver.FirefoxOptions()
    firefox_options.profile = path

    return webdriver.Firefox(options=firefox_options)

def get_chrome(path: str, profile: str) -> webdriver.chromium.webdriver.ChromiumDriver:
    """Get the default chrome browser for the current system."""
    logging.info(f"Creating chrome browser from '{path}'...")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'user-data-dir={path}')
    chrome_options.add_argument(f'profile-directory={profile}')

    return webdriver.Chrome(options=chrome_options)

def get_browser() -> webdriver.chromium.webdriver.ChromiumDriver | webdriver.remote.webdriver.WebDriver:
    """Return the proper browser that will be used based on the
    configuration.
    """
    global config

    default_browser = config['default_browser']

    if default_browser == "firefox":
        return get_firefox(config['firefox_profile_path'])
    elif default_browser == "chrome":
        return get_chrome(config['chrome_userdata_path'], config['chrome_profile'])
    else:
        raise ValueError(
            f"Browser not supported as stated in config '{default_browser}'"
        )

    return webdriver.Firefox()

def run_edenred_page(
        browser: webdriver.chromium.webdriver.ChromiumDriver | webdriver.remote.webdriver.WebDriver
    ) -> None:
    """Run the edenred web page.
    """
    global config

    edenred_automation = EdenredAutomation(config, browser)

    if edenred_automation.download_table_as_csv():
        logging.info("Edenred report download completed.")
    else:
        logging.warning("Edenred report NOT donwloaded.")

def run_uber_page(
        browser: webdriver.chromium.webdriver.ChromiumDriver | webdriver.remote.webdriver.WebDriver
    ) -> None:
    """Run the uber web page.
    """
    global config

    uber_automation = UberAutomation(config, browser)

    if uber_automation.download_last_settlement():
        logging.info("Uber report download completed.")
    else:
        logging.warning("Uber report NOT downloaded!")

def run_browser() -> None:
    """Run the browser where the work will be done.
    """
    global config

    logging.info("Starting browser...")
    browser = get_browser()

    try:
        run_uber_page(browser)

        run_edenred_page(browser)
    finally:
        logging.info("Closing browser...")
        browser.close()

def run() -> int:
    """Run the main program."""
    try:
        set_config()
        config_logging()

        logging.info("Running main program...")

        run_browser()

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
    except ValueError as ve:
        logging.error(ve)

        return 3

if __name__ == '__main__':
    sys.exit(run())
