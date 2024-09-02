"""
Фикстуры для проекта
"""
import json

import pytest
from helpers import make_storage_state_data, make_cokies
from page_objects.auth_page import As
from playwright.sync_api import Page


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
def auth(playwright, page: Page):
    browser = playwright.chromium.launch(headless=False)

    class AuthorizedPage:
        def wrapper(self, auth_type: As):
            access_token, refresh_token = auth_type.tokens()
            access_payload, refresh_payload = auth_type.payload()
            storage_state_data = make_storage_state_data(access_payload, refresh_payload)
            with open("state.json", "w") as f:
                json.dump({"origins": [storage_state_data]}, f)
            context = browser.new_context(storage_state="state.json")
            cookies = make_cokies(access_token, refresh_token)
            context.add_cookies(cookies)
            page = context.new_page()
            return page

    page = AuthorizedPage()

    yield page.wrapper

    browser.close()
