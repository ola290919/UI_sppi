import os

import allure
from playwright.sync_api import expect, Page
from utils.pw_helpers import fill_and_check_value, fill_and_check_value_time


class BlaPage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = os.getenv('BASE_URL_RC')
        self.input_name = self.page.locator('//input[@formcontrolname="name"]')
        self.input_weight_exact = self.page.locator('//input[@type="number" and @formcontrolname="value"]')
        self.input_aircraft_identification = (self.page.
                                              locator('//input[@formcontrolname = "aircraftIdentification"]'))
        self.input_registration_number = (self.page.
                                          locator('//input[@formcontrolname = "registrationNumber"]'))
        self.input_serial_number = self.page.locator('//input[@formcontrolname = "serialNumber"]')
        self.input_pilot_licence = self.page.locator('//input[@formcontrolname = "remotePilotLicence"]')
        self.input_model_bvs = (self.page.
                                locator('//als-select-with-search[@formcontrolname="model"]').
                                locator('//input[@placeholder="Поиск..."]'))
        self.field_text_not_found = self.page.get_by_text('Не найдено')
        self.input_opr = self.page.locator('//input[@formcontrolname = "opr"]')
        self.input_max_flight_time = (self.page.locator('//als-time-input[@formcontrolname="maxFlightTime"]').
                                      locator('//input[@placeholder="ЧЧ:ММ"]'))
        self.input_max_flight_range_value = self.page.locator(
            '//mat-form-field[@formgroupname="maxFlightDistance"]').locator(
            '//input[@formcontrolname="value"]')
        self.input_level_1_value = (self.page.locator('//mat-form-field[@formgroupname="level1"]').
                                    locator('//input[@formcontrolname="value"]'))
        self.input_level_2_value = (self.page.locator('//mat-form-field[@formgroupname="level2"]').
                                    locator('//input[@formcontrolname="value"]'))
        self.button_save = self.page.get_by_role("button", name="Сохранить")
        self.pop_up_save_bla = self.page.get_by_text('BLA создан')
        self.select_weight_category = self.page.locator('//mat-select[@formcontrolname="weightCategory"]')
        self.dropdown_max_flight_range_unit = (self.page.
                                               locator('//mat-form-field[@formgroupname="maxFlightDistance"]').
                                               locator('//als-unit-selector[@formcontrolname="unit"]'))
        self.dropdown_level_1_unit = (self.page.locator('//mat-form-field[@formgroupname="level1"]').
                                      locator('//als-unit-selector[@formcontrolname="unit"]'))
        self.dropdown_level_2_unit = (self.page.locator('//mat-form-field[@formgroupname="level2"]').
                                      locator('//als-unit-selector[@formcontrolname="unit"]'))

    def fill_name(self, value: str):
        fill_and_check_value(self.input_name, value)

    def fill_weight_exact(self, value: str):
        fill_and_check_value(self.input_weight_exact, value)

    def fill_aircraft_identification(self, value: str):
        fill_and_check_value(self.input_aircraft_identification, value)

    def fill_pilot_licence(self, value: str):
        fill_and_check_value(self.input_pilot_licence, value)

    def fill_registration_number(self, value: str):
        fill_and_check_value(self.input_registration_number, value)

    def fill_serial_number(self, value: str):
        fill_and_check_value(self.input_serial_number, value)

    def fill_model_bvs(self, value: str):
        fill_and_check_value(self.input_model_bvs, value)

    def fill_opr(self, value: str):
        fill_and_check_value(self.input_opr, value)

    def fill_max_flight_time(self, hh: str, mm: str):
        fill_and_check_value_time(self.input_max_flight_time, hh, mm)

    def fill_max_flight_range_value(self, value: str):
        fill_and_check_value(self.input_max_flight_range_value, value)

    def fill_level_1_value(self, value: str):
        fill_and_check_value(self.input_level_1_value, value)

    def fill_level_2_value(self, value: str):
        fill_and_check_value(self.input_level_2_value, value)

    @allure.step("Выбрать в выпадающем списке значение {category}")
    def choose_weight_category(self, category):
        self.select_weight_category.dblclick()
        self.page.get_by_role('listbox').get_by_text(category).click()
        expect(self.select_weight_category).to_contain_text(category)
        return self

    @allure.step("Выбрать в выпадающем списке значение {unit}")
    def choose_max_flight_range_unit(self, unit):
        self.dropdown_max_flight_range_unit.click()
        self.page.get_by_role("menuitem", name=unit, exact=True).click()
        expect(self.dropdown_max_flight_range_unit).to_contain_text(unit)
        return self

    @allure.step("Выбрать в выпадающем списке значение {unit}")
    def choose_level_1_unit(self, unit):
        self.dropdown_level_1_unit.click()
        self.page.locator("#mat-menu-panel-3").get_by_role("menuitem", name=unit).click()
        expect(self.dropdown_level_1_unit).to_contain_text(unit)
        return self

    @allure.step("Выбрать в выпадающем списке значение {unit}")
    def choose_level_2_unit(self, unit):
        self.dropdown_level_2_unit.click()
        self.page.locator("#mat-menu-panel-4").get_by_role("menuitem", name=unit).click()
        expect(self.dropdown_level_2_unit).to_contain_text(unit)
        return self

    @allure.step("Перейти на страницу создания БЛА")
    def go_create_bla_page(self):
        self.page.goto(f'{self.base_url}/aircraft/bla/bla/create')
        expect(self.page).to_have_title('СППИ - Воздушные суда - БВС - Добавить')
        return self

    @allure.step("Нажать кнопку Сохранить")
    def click_save_button(self):
        self.button_save.click()
        expect(self.pop_up_save_bla).to_be_visible()
        return self

    @allure.step("Проверить титул страницы грида Воздушные суда - БВС")
    def check_title_grid_page(self):
        expect(self.page).to_have_title('СППИ - Воздушные суда - БВС - Список')
        return self

    def check_created_bla(self, bla_name):
        expect(self.page.get_by_title(bla_name)).to_be_visible()
        return self
