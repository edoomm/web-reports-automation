"""The Uber automation module"""
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        self.config = config
        self.browser = browser

        logging.info(f"Redirecting to {self.config['uber_url']}")
        self.browser.get(self.config['uber_url'])

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

    def select_last_settlement(self) -> None:
        """Select last settlement.

        As of 2024-01-26 the last settlement is selected by default, some
        tests were ran in order to try to select other settlements but none of
        them were succesful.
        """
        pass

    def wait_generation(self) -> None:
        """Wait for report to be generated."""
        logging.info("Waiting for report generation...")
        WebDriverWait(self.browser, self.config['generation_timeout']).until(
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

            time.sleep(2)

            self.click_first_row_download()
            logging.info("Download completed.")

            return True
        except Exception as e:
            logging.error(e)

            return False
