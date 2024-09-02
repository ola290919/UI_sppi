import os

from playwright.sync_api import expect, Page


class BlaPage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = os.getenv('BASE_URL_RC')
        self.input_name = self.page.locator('//input[@formcontrolname="name"]')
        self.input_weight_exact = self.page.locator('//input[@type="number" and @formcontrolname="value"]')
        self.aircraft_identification = self.page.locator('//input[@formcontrolname = "aircraftIdentification"]')
        self.registration_number = self.page.locator('//input[@formcontrolname = "registrationNumber"]')
        self.serial_number = self.page.locator('//input[@formcontrolname = "serialNumber"]')
        self.pilot_licence = self.page.locator('//input[@formcontrolname = "remotePilotLicence"]')
        self.model_bvs = self.page.locator('//als-select-with-search[@formcontrolname="model"]').locator(
            '//input[@placeholder="Поиск..."]')
        self.field_text_not_found = self.page.get_by_text('Не найдено')
        self.opr = self.page.locator('//input[@formcontrolname = "opr"]')
        self.max_flight_time = self.page.locator('//input[@data-testid="alsTimeInputElement"]')
        self.max_flight_range_value = self.page.locator('//mat-form-field[@formgroupname="maxFlightDistance"]').locator(
            '//input[@formcontrolname="value"]')
        self.level_1_value = self.page.locator('//mat-form-field[@formgroupname="level1"]').locator(
            '//input[@formcontrolname="value"]')
        self.level_2_value = self.page.locator('//mat-form-field[@formgroupname="level2"]').locator(
            '//input[@formcontrolname="value"]')
        self.button_save = self.page.get_by_role("button", name="Сохранить")
        self.pop_up_save_bla = self.page.get_by_text('BLA создан')

    def choose_weight_category(self, category):
        self.page.locator('//mat-select[@formcontrolname="weightCategory"]').dblclick()
        self.page.get_by_role('listbox').get_by_text(category).click()
        self.page.locator('//mat-select[@formcontrolname="weightCategory"]').get_by_text(category)
        return self

    def choose_max_flight_range_unit(self, unit):
        self.max_flight_range_unit = self.page.locator('//mat-form-field[@formgroupname="maxFlightDistance"]').locator(
            '//als-unit-selector[@formcontrolname="unit"]')
        self.max_flight_range_unit.click()
        self.page.get_by_role("menuitem", name=unit, exact=True).click()
        self.max_flight_range_unit.get_by_text(unit)
        return self

    def choose_level_1_unit(self, unit):
        self.level_1_unit = self.page.locator('//mat-form-field[@formgroupname="level1"]').locator(
            '//als-unit-selector[@formcontrolname="unit"]')
        self.level_1_unit.click()
        self.page.get_by_role("menuitem", name=unit).click()
        self.level_1_unit.get_by_text(unit)
        return self

    def choose_level_2_unit(self, unit):
        self.level_2_unit = self.page.locator('//mat-form-field[@formgroupname="level2"]').locator(
            '//als-unit-selector[@formcontrolname="unit"]')
        self.level_2_unit.click()
        self.page.locator("#mat-menu-panel-4").get_by_role("menuitem", name=unit).click()
        self.level_2_unit.get_by_text(unit)
        return self

    def go_create_bla_page(self):
        self.page.goto(f'{self.base_url}/aircraft/bla/bla/create')
        expect(self.page).to_have_title('СППИ - Воздушные суда - БВС - Добавить')
        return self

    def click_save_button(self):
        self.button_save.click()
        expect(self.pop_up_save_bla).to_be_visible()
        return self

    def check_title_grid_page(self):
        expect(self.page).to_have_title('СППИ - Воздушные суда - БВС - Список')
        return self

    def check_created_bla(self, bla_name):
        expect(self.page.get_by_title(bla_name)).to_be_visible()
        return self
