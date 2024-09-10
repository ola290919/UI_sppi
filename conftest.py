import json

import allure
import pytest
from playwright.sync_api import Page
from utils.sppi_api_client import SppiApiClient
from utils.sppi_auth_client import SppiAuthClient


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != 'passed':
        item.status = 'failed'
    else:
        item.status = 'passed'


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False, args=["--maximized"])

    yield browser

    browser.close()


@pytest.fixture(scope="session")
def pilot_context(browser):
    sppi_auth_client = SppiAuthClient()
    access_token, refresh_token = sppi_auth_client.pilot_tokens()
    access_payload, refresh_payload = sppi_auth_client.pilot_payload()
    storage_state_data = sppi_auth_client.make_storage_state_data(access_payload, refresh_payload)
    with open("state.json", "w") as f:
        json.dump({"origins": [storage_state_data]}, f)
    cookies = sppi_auth_client.make_cokies(access_token, refresh_token)
    context = browser.new_context(storage_state="state.json")
    context.add_cookies(cookies)

    yield context

    context.close()


@pytest.fixture(scope="function")
def pilot_page(pilot_context, request):
    page: Page
    page = pilot_context.new_page()

    yield page

    if request.node.status == 'failed':
        allure.attach(body=page.url, name="URL", attachment_type=allure.attachment_type.URI_LIST)
        allure.attach(page.screenshot(full_page=True), name="Screen shot on failure",
                      attachment_type=allure.attachment_type.PNG)

    page.close()


@pytest.fixture(scope="session")
def atm_dispatcher_moscow_context(browser):
    sppi_auth_client = SppiAuthClient()

    access_token, refresh_token = sppi_auth_client.atm_dispatcher_moscow_tokens()
    access_payload, refresh_payload = sppi_auth_client.atm_dispatcher_moscow_payload()
    storage_state_data = sppi_auth_client.make_storage_state_data(access_payload, refresh_payload)
    with open("state.json", "w") as f:
        json.dump({"origins": [storage_state_data]}, f)
    cookies = sppi_auth_client.make_cokies(access_token, refresh_token)
    context = browser.new_context(storage_state="state.json")
    context.add_cookies(cookies)

    yield context

    context.close()


@pytest.fixture(scope="function")
def atm_dispatcher_moscow_page(atm_dispatcher_moscow_context, request):
    page: Page
    page = atm_dispatcher_moscow_context.new_page()

    yield page

    if request.node.status == 'failed':
        allure.attach(body=page.url, name="URL", attachment_type=allure.attachment_type.URI_LIST)
        allure.attach(page.screenshot(full_page=True), name="Screen shot on failure",
                      attachment_type=allure.attachment_type.PNG)

    page.close()


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
