"""The automation module."""
import json
import logging

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Automation:
    """Control webpages."""

    def __init__(
            self, config: dict, webpage_config_name: str,
            browser: webdriver.Firefox | webdriver.Chrome
        ) -> None:
        """
        Create a new automation instance.

        :param config: The user and webpage configuration.
        :param webpage_config_name: The name of the webpage configuration file.
        :param browser: The created browser by selenium.
        """
        self.config = config | self.get_webpage_config(webpage_config_name)
        self.browser = browser

        logging.info(f"Redirecting to '{self.config['url']}")
        self.browser.get(self.config['url'])

    def get_webpage_config(self, file_name: str) -> dict:
        """
        Get the webpage configuration.

        :param file_name: The name of the configuration file inside the config
        directory.
        :return: The configuration as a dictionary.
        """
        if ".json" not in file_name: file_name += ".json"

        logging.info(f"Retrieving config file: {file_name}...")

        with open(f'config/{file_name}', 'r') as config_file:
            config = json.load(config_file)

        return config

    def perform_click(self, locator: tuple[str, str]) -> None:
        """
        Perform a click to an element based on the locator provided.

        :param locator: A tuple that contains a By strategy and its
        correspondant value for finding an element.
        """
        logging.info(f"Clicking {locator}...")

        WebDriverWait(self.browser, self.config['click_timeout']).until(
            EC.element_to_be_clickable(locator)
        ).click()
