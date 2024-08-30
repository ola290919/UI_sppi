"""
Тесты проверки сценариев
"""
import time
import pytest
import allure
from page_objects.base_page import BasePage
from playwright.sync_api import Page, expect, Locator



@allure.feature('Authorization/registration')
def test_one(page: Page, auth_admin):
    base = BasePage(page, auth_admin)
    base.go_profile()




