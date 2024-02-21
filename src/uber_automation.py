"""The Uber automation module"""
import time
import json
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class UberAutomation:
    """Controls the Uber webpage for gathering the necessary data for making
    reports.
    """

    def __init__(
            self,
            config: object,
            browser: webdriver.chromium.webdriver.ChromiumDriver | webdriver.remote.webdriver.WebDriver
        ) -> None:
        """Create a new automation for the Uber webpage.
        """
        self.config = config | self.get_uber_config()
        self.browser = browser

        logging.info(f"Redirecting to {self.config['url']}")
        self.browser.get(self.config['url'])

    def get_uber_config(self) -> dict:
        """Get the uber config."""
        with open('config/uber.json', 'r') as config_file:
            config = json.load(config_file)

        return config

    def btn_locator(self, data_tracking_name: str) -> tuple[str, str]:
        """Locator for buttons."""
        return (
            By.XPATH, f'//button[@data-tracking-name="{data_tracking_name}"]'
        )

    def e_locator(self, class_name: str) -> tuple[str, str]:
        """Locator for pressable elements."""
        return (By.CLASS_NAME, f'{class_name}')

    def o_locator(self, class_name: str, option_text: str) -> tuple[str, str]:
        """Locator for options within a dropdown"""
        option_xpath = f'//div[@class="{class_name}" and text()="{option_text}"]'
        return (By.XPATH, option_xpath)

    def perform_click(self, locator: tuple[str, str]) -> None:
        """Performs a click to a button or pressable element based on the
        locator provided.
        """
        WebDriverWait(self.browser, self.config['click_timeout']).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def change_report_type(self) -> None:
        """Change the report type based on the configuration."""
        # Clicking dropdown
        logging.info(
            f"Clicking dropdown menu '{self.config['dropdown_report_class']}'..."
        )
        self.perform_click(
            self.e_locator(self.config['dropdown_report_class'])
        )

        time.sleep(self.config['general_timeout'] - 1)

        # Clicking option
        logging.info(
            f"Selecting '{self.config['report_option_text'],}' "
            + f"option from '{self.config['report_option_class']}'"
        )
        self.perform_click(
            self.o_locator(
                self.config['report_option_class'],
                self.config['report_option_text']
            )
        )

    def change_focus(self) -> None:
        """Change focus to the next element.

        Works as if the <TAB> key was pressed.
        """
        self.browser.switch_to.active_element.send_keys(Keys.TAB)

    def select_settlement(self, jumps=3) -> None:
        """Select settlement from given week.

        A direct identification of the dropdown menu through its class name it
        is not possible, therefore this function will only work after
        `change_report_type` is used or the report type dropdown element has
        the current focus.
        """
        logging.info("Executing `select_settlement` function...")
        # When `jumps=3` it is assumed that the active element is the report
        # dropdown
        for i in range(jumps): self.change_focus()

        # Opening dates dropdown
        logging.info("Attempting to open dates dropdown...")
        self.browser.switch_to.active_element.send_keys(Keys.SPACE)

        time.sleep(self.config['general_timeout'] - 1)

        logging.info(f"Selecting week: {self.config['week']}...")
        ul_element = WebDriverWait(
            self.browser, self.config['generation_timeout']
        ).until(
            EC.presence_of_element_located(
                self.e_locator(self.config['dates_dropdown_class'])
            )
        )
        li_elements = ul_element.find_elements(By.XPATH, './/li')
        # Doing the actual select
        li_elements[self.config['week'] - 1].click()

    def wait_generation(self) -> None:
        """Wait for report to be generated."""
        timeout = self.config['generation_timeout']
        logging.info(f"Waiting for report generation for {timeout}s...")
        WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[role="alert"][data-baseweb="toast"]')
            )
        )

    def click_first_row_download(self) -> None:
        """Click the first button from the first row to download the last
        report."""
        logging.info("Clicking first download...")

        logging.info("Getting first row of downloads table...")
        rows = self.browser.find_elements(
            By.XPATH,
            '//div[@role="row" and @data-testid="payment-reporting-table-row"]'
        )

        first_row = rows[10]

        logging.info("Performing click on first donwload...")
        download_button = first_row.find_element(
            By.XPATH, './/button[@data-testid="download-report-button"]'
        )
        download_button.click()

    def download_last_settlement(self) -> bool:
        """Download the last report according to the current settlement."""
        try:
            self.change_report_type()

            logging.info("Clicking generate button...")
            self.perform_click(self.btn_locator("generate"))

            self.wait_generation()

            time.sleep(self.config['general_timeout'])

            self.click_first_row_download()

            time.sleep(self.config['general_timeout'])

            logging.info("Download completed.")

            return True
        except Exception as e:
            logging.error(e)

            return False
