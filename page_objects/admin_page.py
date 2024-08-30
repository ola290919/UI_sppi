"""
Базовый класс для всех страниц
"""
import allure
import os
from playwright.sync_api import expect, Locator, Page


class AdminPage():
    """Базовый класс"""

    def __init__(self, page: Page, auth_admin):

        self.page = page
        self.admin_page = auth_admin


    def go_profile_admin(self):
        self.admin_page.goto('http://app.sppi.dev.plan/profile')
        expect(self.admin_page).to_have_title('СППИ - Профиль')
        return self
