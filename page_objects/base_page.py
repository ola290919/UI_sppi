"""
Базовый класс для всех страниц
"""
import os

from dotenv import load_dotenv
from playwright.sync_api import Page

load_dotenv()


class BasePage():
    """Базовый класс"""

    def __init__(self, page: Page):
        self.page = page
        self.base_url = os.getenv('BASE_URL_RC')

    def input_value_by_letter(self, locator: str, text: str):
        """Заполнить поле"""
        self.page.locator(locator).clear()
        for l in text:
            self.page.wait_for_selector(locator).press(l)
