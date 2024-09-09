import os
import allure

from playwright.sync_api import expect, Page
from utils.pw_helpers import fill_and_check_value, fill_and_check_value_time


class FplPage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = os.getenv('BASE_URL_RC')
        self.modal_confirm = (self.page.
                              get_by_text('Вы работали с этой формой, восстановить информацию?'))
        self.no_button_in_confirm_modal = self.page.get_by_role(
            "button", name="Нет, очистить информацию")
        self.input_reg_number = (self.page.
                                 locator('//als-select-with-search[@formcontrolname="field7"]').
                                 locator('//input[@placeholder]'))
        self.input_type_aircraft = (self.page.locator(
            '//als-select-with-search[@formcontrolname="typeOfAircraft"]').
                                    locator('//input[@placeholder="Поиск..."]'))
        self.input_equipment = self.page.locator('//input[@formcontrolname="field10"]')
        self.input_desc_time = (self.page.locator('//als-time-input[@formcontrolname="time"]').
                                locator('//input[@placeholder="ЧЧ:ММ"]'))
        self.input_level_value = (self.page.locator('//mat-form-field[@formgroupname="level"]').
                                  locator('//input[@formcontrolname="value"]'))
        self.button_specify_route = self.page.get_by_role("button", name="Уточнить маршрут")
        self.ok_button_in_information_modal = self.page.locator(
            '//sppi6-information-before-open-route-modal').get_by_role("button", name="Ок")
        self.textarea_route = self.page.locator('//textarea[@formcontrolname="route"]')
        self.input_duration = (self.page.locator('//als-time-input[@formcontrolname="totalEet"]').
                               locator('//input[@data-testid="alsTimeInputElement"]'))
        self.button_submit = self.page.get_by_role("button", name="Сформировать план")
        self.modal_diagnostic = (self.page.locator('//sppi6-flight-diagnostics').
                                 get_by_text('План полёта сформирован.'))
        self.text_fpl_in_diagnostic_modal = (self.page.locator('//sppi6-flight-diagnostics').
                                             locator('//pre'))
        self.button_send_fpl = self.page.get_by_role("button", name="Отправить план")
        self.modal_sent_success = (self.page.locator('//sppi6-plan-sent-success').
                                   get_by_text('План успешно отправлен в: Московский центр ЕС ОрВД'))
        self.select_fpl_type = self.page.locator('//mat-select[@formcontrolname="fplType"]')
        self.select_flight_rules = self.page.locator('//mat-select[@formcontrolname="flightRules"]')
        self.select_flight_type = self.page.locator('//mat-select[@formcontrolname="typeOfFlight"]')
        self.field_aircraft_type = self.page.locator(
            '//als-select-with-search[@formcontrolname="typeOfAircraft"]')
        self.select_turbulence_cat = (self.page.
                                      locator('//mat-select[@formcontrolname="wakeTurbulenceCat"]'))
        self.field_aerodrom_dep = (self.page.
                                   locator('//mat-form-field[@formgroupname="field13"]').
                                   locator('//als-select-with-search[@formcontrolname="aerodrome"]'))
        self.dropdown_level_unit = (self.page.
                                    locator('//mat-form-field[@formgroupname="level"]').
                                    locator('//als-unit-selector[@formcontrolname="unit"]'))
        self.field_aerodrom_arr = (self.page.
                                   locator('//mat-form-field[@formgroupname="field16"]').
                                   locator('//als-select-with-search[@formcontrolname="aerodrome"]'))

    @allure.step("Перейти на страницу создания FPL")
    def go_create_fpl_page(self):
        self.page.goto(f'{self.base_url}/plans/fpl/create')
        expect(self.page).to_have_title('СППИ - Планы ИВП - FPL - Создать')
        return self

    @allure.step("При появления окна подтверждения нажать Нет, очистить информацию")
    def close_confirm_modal(self):
        if self.modal_confirm.is_visible():
            self.no_button_in_confirm_modal.click()
        else:
            pass

    def fill_reg_number(self, value: str):
        fill_and_check_value(self.input_reg_number, value)

    def fill_equipment(self, value: str):
        fill_and_check_value(self.input_equipment, value)

    def fill_level_value(self, value: str):
        fill_and_check_value(self.input_level_value, value)

    def fill_route(self, value: str):
        fill_and_check_value(self.textarea_route, value)

    def fill_desc_time(self, hh: str, mm: str):
        fill_and_check_value_time(self.input_desc_time, hh, mm)

    def fill_duration(self, hh: str, mm: str):
        fill_and_check_value_time(self.input_duration, hh, mm)

    @allure.step("Выбрать в выпадающем списке значение {fpl_type}")
    def choose_fpl_type(self, fpl_type):
        self.select_fpl_type.dblclick()
        self.page.get_by_role('option').get_by_text(fpl_type).click()
        expect(self.select_fpl_type).to_contain_text(fpl_type)
        return self

    @allure.step("Выбрать в выпадающем списке значение {rules}")
    def choose_flight_rules(self, rules):
        self.select_flight_rules.dblclick()
        self.page.get_by_role('option').get_by_text(rules).click()
        expect(self.select_flight_rules).to_contain_text(rules)
        return self

    @allure.step("Выбрать в выпадающем списке значение {flight_type}")
    def choose_flight_type(self, flight_type):
        self.select_flight_type.dblclick()
        self.page.get_by_role('listbox').get_by_text(flight_type).click()
        expect(self.select_flight_type).to_contain_text(flight_type)
        return self

    @allure.step("Заполнить поле с выпадающим списком значением {aircraft_type}")
    def fill_aircraft_type(self, aircraft_type):
        self.field_aircraft_type.locator('//input[@placeholder="Поиск..."]').fill(aircraft_type)
        self.page.get_by_role('listbox').get_by_text(aircraft_type).click()
        expect(self.field_aircraft_type).to_contain_text(aircraft_type)
        return self

    @allure.step("Выбрать в выпадающем списке значение {cat}")
    def choose_turbulence_cat(self, cat):
        self.select_turbulence_cat.dblclick()
        self.page.get_by_role('listbox').get_by_text(cat).click()
        expect(self.select_turbulence_cat).to_contain_text(cat)
        return self

    @allure.step("Заполнить поле с выпадающим списком значением {aerodrom_name}")
    def fill_aerodrome_dep(self, aerodrom_name):
        self.field_aerodrom_dep.locator('//input[@placeholder="Поиск..."]').fill(aerodrom_name)
        self.page.get_by_role('listbox').get_by_text(aerodrom_name).click()
        expect(self.field_aerodrom_dep).to_contain_text(aerodrom_name)
        return self

    @allure.step("Выбрать в выпадающем списке значение {unit}")
    def choose_level_unit(self, unit):
        self.dropdown_level_unit.click()
        self.page.get_by_role("menuitem", name=unit).click()
        expect(self.dropdown_level_unit).to_contain_text(unit)
        return self

    @allure.step("Заполнить поле с выпадающим списком значением {aerodrom_name}")
    def fill_aerodrome_arr(self, aerodrom_name):
        self.field_aerodrom_arr.locator('//input[@placeholder="Поиск..."]').fill(aerodrom_name)
        self.page.get_by_role('listbox').get_by_text(aerodrom_name).click()
        expect(self.field_aerodrom_arr).to_contain_text(aerodrom_name)
        return self
