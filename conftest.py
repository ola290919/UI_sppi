"""
Фикстура для проекта
"""
from typing import Dict

import allure
import pytest
import requests
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Item
from playwright.sync_api import Page, Playwright
from playwright.sync_api import sync_playwright

import pytest
from page_objects.auth_page import AuthPage



# @pytest.fixture(autouse=True)
# def attach_playwright_results(page: Page, request: FixtureRequest):
#     """Fixture to perform teardown actions and attach results to Allure report
#     on failure.
#     """
#     yield
#     if request.node.rep_call.failed:
#         allure.attach(
#             body=page.url,
#             name="URL",
#             attachment_type=allure.attachment_type.URI_LIST,
#         )
#         allure.attach(
#             page.screenshot(full_page=True),
#             name="Screen shot on failure",
#             attachment_type=allure.attachment_type.PNG,
#         )


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item: Item):
#     """Hook implementation to generate test report for each test phase.
#     """
#     outcome = yield
#     rep = outcome.get_result()
#     setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture()
def auth_admin(playwright, page: Page):

    browser = playwright.chromium.launch(channel="chrome", headless=False)

    token = AuthPage().as_admin()

    context = browser.new_context()
    context.add_cookies([{'name': 'refresh_token', 'value': token, 'url': 'http://app.sppi.dev.plan'},
                         {'name': 'authorization', 'value': token, 'url': 'http://app.sppi.dev.plan'}])

    page = context.new_page()
    yield page
    page.close()
    browser.close()


