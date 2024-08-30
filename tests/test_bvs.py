"""
Тесты проверки сценариев
"""
import time
import datetime
import pytest
import allure
from page_objects.admin_page import AdminPage
from page_objects.auth_page import AuthPage
from page_objects.pilot_page import PilotPage

from playwright.sync_api import Page, expect, Locator
from playwright.sync_api import Page, Playwright
from playwright.sync_api import sync_playwright


@allure.feature('Authorization/registration')
def test_one(page: Page, auth_admin, auth_pilot):
    admin = AdminPage(page, auth_admin)
    admin.go_profile_admin()
    pilot = PilotPage(page, auth_pilot)
    pilot.go_profile_pilot()

def test_profile_page_title():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        expires = int((datetime.datetime.now() + datetime.timedelta(minutes=3)).timestamp())
        access_token, refresh_token = AuthPage().as_admin()

        context.add_cookies([
            {
                'name': 'refresh_token',
                'value': refresh_token,
                'path': '/',
                'domain': 'http://app.sppi.dev.plan',
                'httpOnly': True,
                'secure': False,
                'sameSite': 'Strict',
                'expires': expires
            },
            {
                'name': 'authorization',
                'value': access_token,
                'path': '/',
                'domain': 'http://app.sppi.dev.plan',
                'httpOnly': True,
                'secure': False,
                'sameSite': 'Strict',
                'expires': expires
            }
        ])
        page = context.new_page()
        page.goto("http://app.sppi.dev.plan/profile")
        time.sleep(5)
        assert page.title() == "СППИ - Профиль"
        browser.close()
