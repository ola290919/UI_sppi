"""
Тесты проверки сценариев
"""
import time

import allure
from page_objects.auth_page import As
from page_objects.bla_page import BlaPage


class TestBlaCreate():
    @allure.feature('')
    def test_bla_up_to_0_15(self, auth):
        bla = BlaPage(auth(As.PILOT))
        bla.go_create_bla_page().input_form_up_to_0_15_kg().click_save_button().check_created_bla()
        time.sleep(10)

    def test_bla_from_0_15_up_to_30(self, auth):
        bla = BlaPage(auth(As.PILOT))
        bla.go_create_bla_page().input_form_from_0_15_up_to_30_kg().click_save_button().check_created_bla()

    def test_bla_more_than_30(self, auth):
        bla = BlaPage(auth(As.PILOT))
        bla.go_create_bla_page().input_form_more_than_30_kg().click_save_button().check_created_bla()

