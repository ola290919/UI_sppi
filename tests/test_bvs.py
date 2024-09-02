"""
Тесты проверки сценариев
"""
import allure
from page_objects.auth_page import As
from page_objects.bla_page import BlaPage


# class BlaCreateTests:
@allure.feature('')
def test_bla_undo_0_15(page, auth):
    bla = BlaPage(auth(As.PILOT))
    bla.go_create_bla_page().input_form_up_to_0_15_kg().click_save_button().check_created_bla()
