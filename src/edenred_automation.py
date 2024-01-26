import csv
import time
import os.path
import logging
from io import StringIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class EdenredAutomation:
    """Controls the Edenred webpage."""

    def __init__(
            self,
            config: object,
            browser: webdriver.chromium.webdriver.ChromiumDriver | webdriver.remote.webdriver.WebDriver
        ) -> None:
        """Create a new automation for the Uber webpage.
        """
        self.config = config
        self.browser = browser

        logging.info(f"Redirecting to {self.config['edenred_url']}")
        self.browser.get(self.config['edenred_url'])

    def change_selects(self) -> None:
        """Change select options for identifier and transaction selects."""
        logging.info("Changing select options...")

        # Identifier select
        Select(self.browser.find_element(
            By.ID, self.config['edenred_id_select_id']
        )).select_by_value(self.config['edenred_id_select_id'])
        # Transaction select
        Select(self.browser.find_element(
            By.ID, self.config['edenred_transaction_select_id']
        )).select_by_value(self.config['edenred_transaction_select_id'])

    def change_text(self, input_id: str, text: str) -> None:
        """Change text for given input."""
        logging.info(f"Changing text '{text}' to input '{input_id}'")

        input_element = self.browser.find_element(By.ID, input_id])
        input_element.clear()
        input_element.send_keys(text)

    def change_dates(self) -> None:
        """Change start and end dates from inputs."""
        # Calculates dates as settlements
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=end_date.weekday())

        # Changing dates
        f = "%d/%m/%Y"
        self.change_text(self.config['edenred_startdate_id'], start_date.strftime(f))
        self.change_text(self.config['edenred_enddate_id'], end_date.strftime(f))

    def get_table(self) -> list[str]:
        """Get transactions table as list."""
        logging.info("Getting transactions table data...")

        table = self.browser.find_element(
            By.ID, self.config['edenred_table_id']
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

        return table_data

    def download_table_as_csv(self) -> bool:
        """Download transactions table as csv."""
        try:
            # Changing necessary data
            self.change_selects()
            self.change_dates()
            
            time.sleep(2)

            # Clicking consult button
            self.browser.find_element(
                By.ID, self.config['edenred_consult_btn_id']
            ).click

            time.sleep(2)

            # Transforming table to csv
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

            csv_filename = f"edenred_{datetime.now.date()}.csv"
            file_path = os.path.join(self.config['download_path'], csv_filename)
            logging.info(f"Saving csv to {file_path}")

            with open(file_path, "w", newline="") as csv_file:
                csv_file.write(csv_output.getvalue())

            logging.info("Download completed.")

            return True
        except Exception as e:
            logging.error(e)

            return False
