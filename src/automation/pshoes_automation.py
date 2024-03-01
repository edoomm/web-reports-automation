from selenium import webdriver
from selenium.webdriver.common.by import By

from automation.automation import Automation

class PriceShoesAutomation(Automation):
    """Control the Price Shoes webpage."""

    def __init__(self, config: dict,
            browser: webdriver.Firefox | webdriver.Chrome,
            webpage_config_name="pshoes.json"
        ) -> None:
        """
        Create a new automation for the Price Shoes webpage.

        :param config: The configuration file.
        :param browser: A firefox or chrome webdriver instance
        :param webpage_config_name str: The price shoes configuration
        file name.
        """
        super().__init__(config, webpage_config_name, browser)
        self.product_ids = []

    def retrieve_product_ids(self):
        """
        Retrieve all the product IDs contained in the website.

        Withouth scrolling it gives 18 product IDs.
        """
        products_container = self.browser.find_element(
            By.CLASS_NAME, self.config['products_container_class']
        )
        product_elements = products_container.find_elements(
            By.CLASS_NAME, self.config['product_elements_class']
        )

        self.product_ids = [
            element.find_element(By.XPATH, ".//span[@class='select-all']").text.strip()
            for element in product_elements
        ]
