import csv
import time
import json
import os.path
import logging
from io import StringIO
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EdenredAutomation:
    """Controls the Edenred webpage."""

    def __init__(
            self,
            config: object,
            browser: webdriver.chromium.webdriver.ChromiumDriver | webdriver.remote.webdriver.WebDriver
        ) -> None:
        """Create a new automation for the Uber webpage.
        """
        self.config = config | self.get_edenred_config()
        self.browser = browser

        logging.info(f"Redirecting to '{self.config['url']}'")
        self.browser.get(self.config['url'])

    def get_edenred_config(self) -> dict:
        """Get the edenred config."""
        with open('config/edenred.json', 'r') as config_file:
            config = json.load(config_file)

        return config

    def change_selects(self) -> None:
        """Change select options for identifier and transaction selects."""
        logging.info("Changing select options...")

        # Identifier select
        Select(self.browser.find_element(
            By.ID, self.config['id_select_id']
        )).select_by_value(self.config['id_select_val'])
        # Transaction select
        Select(self.browser.find_element(
            By.ID, self.config['transaction_select_id']
        )).select_by_value(self.config['transaction_select_val'])

    def change_text(self, input_id: str, text: str, log=True) -> None:
        """Change text for given input."""
        if log:
            logging.info(f"Changing text '{text}' to input '{input_id}'")

        input_element = self.browser.find_element(By.ID, input_id)
        input_element.clear()
        input_element.send_keys(text)

    def click_btn(self, btn_id: str, by=By.ID) -> None:
        """Click button."""
        logging.info(f"Clicking '{btn_id}'...")
        self.browser.find_element(By.ID, btn_id).click()

    def login(self) -> None:
        """Log in to Edenred."""
        logging.info("Attempting to log in...")

        with open('config/e_creds', 'r') as file:
            creds = file.read().split('\n')

        self.change_text(self.config['user_name_input_id'], creds[0])

        self.click_btn(self.config['login_btn_id'])

        # Waiting for pass input to appear
        WebDriverWait(self.browser, self.config['appear_timeout']).until(
            EC.visibility_of_element_located(
                (By.ID, self.config['pass_input_id'])
            )
        )

        time.sleep(self.config['login_timeout'])

        self.change_text(self.config['pass_input_id'], creds[1], False)

        self.click_btn(self.config['login_btn_id'])

        logging.info("Log in succesful.")

    def go_to_movements(self) -> None:
        """Go to movements page."""
        time.sleep(self.config['login_timeout'])
        self.login()

        # Click card
        logging.info("Waiting for clickable card to appear...")
        WebDriverWait(self.browser, self.config['click_timeout']).until(
            EC.element_to_be_clickable((By.ID, self.config['card_id']))
        ).click()
        time.sleep(self.config['login_timeout'])
        logging.info("Card clicked.")

        time.sleep(self.config['login_timeout'] + 1)

        logging.info(f"Redirecting to '{self.config['movements_url']}'...")
        self.browser.get(self.config['movements_url'])

    def change_dates(self) -> None:
        """Change start and end dates from inputs."""
        logging.info("Changing dates...")
        # Calculates dates as settlements
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=end_date.weekday())

        # Changing dates
        f = "%d/%m/%Y"
        self.change_text(self.config['start_date_id'], start_date.strftime(f))
        self.change_text(self.config['end_date_id'], end_date.strftime(f))

    def get_table(self) -> list[str]:
        """Get transactions table as list."""
        logging.info("Getting transactions table data...")

        table = self.browser.find_element(
            By.ID, self.config['table_id']
        )

        # Get the table rows
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Initialize a list to store the table data
        table_data = []
        
        # Iterate over the rows and extract the cell data
        for row in rows:
            # Extract cell data from each row
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text for cell in cells]
            
            # Add the row data to the table data list
            table_data.append(row_data)

        table_data.pop(0)

        # Starting 36 row is the actual data
        return table_data[36:]

    def create_csv(self) -> None:
        """Create the csv file to be downloaded."""
        # Transforming table to csv
        logging.info("Waiting for table to appear...")
        WebDriverWait(self.browser, self.config['appear_timeout']).until(
            EC.visibility_of_element_located(
                (By.ID, self.config['table_id'])
            )
        )
        logging.info("Getting table...")
        table_data = self.get_table()

        logging.info("Transforming table to csv...")

        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)

        header = [
            "Acción", "Identificador", "Número de tarjeta", "Tipo Tarjeta",
            "Fecha", "Cant Litros", "Mercancia", "Afiliado", "Saldo Anterior",
            "Monto", "Saldo Actual", "Facturable", "Tipo", "Estatus", "Ajuste", 
            "Controlador volumétrico", "Por Excepción", "Ticket Bomba",
            "Tag NFC", "Tag NFC Numeric", "Viaje", "Observaciones"
        ]
        csv_writer.writerow(header)

        csv_writer.writerows(table_data)

        logging.info("csv file wrote.")

        csv_filename = f"edenred_{datetime.now().date()}.csv"
        file_path = os.path.join(self.config['download_path'], csv_filename)
        logging.info(f"Saving csv to {file_path}")

        with open(file_path, "w", newline="") as csv_file:
            csv_file.write(csv_output.getvalue())


    def download_table_as_csv(self) -> bool:
        """Download transactions table as csv."""
        self.go_to_movements()

        try:
            # Changing necessary data
            self.change_selects()
            self.change_dates()
            
            # Clicking consult button
            logging.info("Clicking consult button...")

            self.browser.find_element(
                By.ID, self.config['consult_btn_id']
            ).click()

            # Creating csv
            self.create_csv()
            logging.info("Download completed.")

            return True
        except Exception as e:
            logging.error(e)

            return False
