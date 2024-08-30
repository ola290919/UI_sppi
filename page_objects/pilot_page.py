"""
Базовый класс для всех страниц
"""
import allure
import os
from playwright.sync_api import expect, Locator, Page


class PilotPage():
    """Базовый класс"""

    def __init__(self, page: Page, auth_pilot):

        self.page = page
        self.pilot_page = auth_pilot



    def go_profile_pilot(self):
        self.pilot_page.goto('http://app.sppi.dev.plan/profile')
        expect(self.pilot_page).to_have_title('СППИ - Профиль')
        return self
