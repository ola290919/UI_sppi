"""
Фикстуры для проекта
"""
import json

import pytest
import allure
from utils.auth_helpers import make_storage_state_data, make_cokies
from utils.sppi_auth_client import As
from utils.sppi_api_client import SppiApiClient
from playwright.sync_api import Page, sync_playwright
from page_objects.shr_message_page import ShrMessagePage


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != 'passed':
        item.status = 'failed'
    else:
        item.status = 'passed'


@pytest.fixture(autouse=True)
def attach_playwright_results(request):
    """Fixture to perform teardown actions and attach results to Allure report
    on failure.
    """
    yield
    page: Page
    if request.node.status == 'failed':
        allure.attach(
            body=page.url,
            name="URL",
            attachment_type=allure.attachment_type.URI_LIST,
        )
        allure.attach(
            page.screenshot(full_page=True),
            name="Screen shot on failure",
            attachment_type=allure.attachment_type.PNG,
        )

def pytest_addoption(parser):
    parser.addoption("--launch_mode", default="remote", choices=["remote", "local"])
    parser.addoption("--br", action="store", default="ch", choices=["ch", "ff"])

@pytest.fixture()
def auth(request):
    with sync_playwright() as playwright:
        browser_name = request.config.getoption("--br")
        if browser_name == "ch":
            browser = playwright.chromium.launch(headless=False)
        elif browser_name == "ff":
            browser = playwright.firefox.launch(headless=False)
        class AuthorizedPage:

            def wrapper(self, auth_type: As) -> Page:
                access_token, refresh_token = auth_type.tokens()
                access_payload, refresh_payload = auth_type.payload()
                storage_state_data = make_storage_state_data(access_payload, refresh_payload)
                with open("state.json", "w") as f:
                    json.dump({"origins": [storage_state_data]}, f)
                self.context = browser.new_context(storage_state="state.json")
                cookies = make_cokies(access_token, refresh_token)
                self.context.add_cookies(cookies)
                self.page = self.context.new_page()
                return self.page

            def close_context(self):
                self.context.close()
                self.page.close()
                return self

        page = AuthorizedPage()

        yield page.wrapper

        page.close_context

        browser.close()

@pytest.fixture(scope="function")
def name_of_sent_shr():
    api_client = SppiApiClient()
    id_shr, name_shr = api_client.get_created_shr_id_name()
    api_client.send_created_shr(id_shr)
    return name_shr

@pytest.fixture(scope="function")
def name_of_ack_shr():
    api_client = SppiApiClient()
    id_shr, name_shr = api_client.get_created_shr_id_name()
    api_client.send_created_shr(id_shr)
    api_client.ack_message_for_shr(id_shr)
    return name_shr

@pytest.fixture(scope="function")
def name_of_dep_shr():
    api_client = SppiApiClient()
    id_shr, name_shr = api_client.get_created_shr_id_name()
    api_client.send_created_shr(id_shr)
    api_client.ack_message_for_shr(id_shr)
    api_client.dep_message_for_shr(id_shr)
    return name_shr




