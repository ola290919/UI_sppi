import os

import allure
from playwright.sync_api import expect, Page


class ShrMessagePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = os.getenv('BASE_URL_RC')
        self.ack_button = self.page.get_by_role('button', name='ACK')
        self.rej_button = self.page.get_by_role('button', name='REJ')
        self.cnl_button = self.page.get_by_role('button', name='CNL')
        self.dep_button = self.page.get_by_role('button', name='DEP')
        self.arr_button = self.page.get_by_role('button', name='ARR')
        self.send_ack_button = self.page.get_by_role('button', name='Сформировать ACK')
        self.send_rej_button = self.page.get_by_role('button', name='Сформировать REJ')
        self.send_cnl_button = self.page.get_by_role('button', name='Подать CNL')
        self.send_dep_button = self.page.get_by_role('button', name='Подать DEP')
        self.send_arr_button = self.page.get_by_role('button', name='Подать ARR')
        self.sent_modal = self.page.locator('//simple-snack-bar/span')

    @allure.step("Нажать кнопку ACK")
    def ack_button_click(self):
        self.ack_button.click()
        return self

    @allure.step("Нажать кнопку REJ")
    def rej_button_click(self):
        self.rej_button.click()
        return self

    @allure.step("Нажать кнопку CNL")
    def cnl_button_click(self):
        self.cnl_button.click()
        return self

    @allure.step("Нажать кнопку DEP")
    def dep_button_click(self):
        self.dep_button.click()
        return self

    @allure.step("Нажать кнопку ARR")
    def arr_button_click(self):
        self.arr_button.click()
        return self

    @allure.step("Перейти на страницу грида Планы ИВП - SHR")
    def go_shr_grid_page(self):
        self.page.goto(f'{self.base_url}/plans/shr')
        expect(self.page).to_have_title('СППИ - Планы ИВП - SHR - Список')
        return self

    @allure.step("Открыть контектное меню SHR с названием {shr_name}")
    def open_context_menu(self, shr_name):
        (self.page.get_by_title(shr_name)
         .locator('xpath=./ancestor::div[@class="grid-row d-flex ng-star-inserted"]')
         .locator('//button[@aria-haspopup="menu"]').click())
        return self

    @allure.step("Отправить ACK на SHR и проверить наличие модального окна")
    def send_ack(self):
        self.send_ack_button.click()
        expect(self.sent_modal).to_contain_text('ACK сформирован')

    @allure.step("Отправить REJ на SHR и проверить наличие модального окна")
    def send_rej(self):
        self.send_rej_button.click()
        expect(self.sent_modal).to_contain_text('REJ сформирован')

    @allure.step("Проверить статус {status} у SHR с названием {shr_name}")
    def check_flight_status(self, shr_name, status):
        (self.page.get_by_title(shr_name)
         .locator('xpath=./ancestor::div[@class="grid-row d-flex ng-star-inserted"]')
         .get_by_title(status)).is_visible()
        return self

    @allure.step("Отправить CNL на SHR и проверить наличие модального окна")
    def send_cnl(self):
        self.send_cnl_button.click()
        expect(self.sent_modal).to_contain_text('CNL сформирован')

    @allure.step("Отправить DEP на SHR и проверить наличие модального окна")
    def send_dep(self):
        self.send_dep_button.click()
        expect(self.sent_modal).to_contain_text('DEP отправлен')

    @allure.step("Отправить ARR на SHR и проверить наличие модального окна")
    def send_arr(self):
        self.send_arr_button.click()
        expect(self.sent_modal).to_contain_text('ARR не отправлен')
