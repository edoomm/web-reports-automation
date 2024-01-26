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

    def __init__(self, browser: webdriver) -> None:
        logging.info("Instiantiating UberAutomation object...")
