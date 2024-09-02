import allure

import os
from playwright.sync_api import expect, Locator, Page
from page_objects.base_page import BasePage
from helpers import random_string


class BlaPage(BasePage):

    BLA_NAME = random_string() + 'AUTOTEST'
    INPUT_NAME = '//input[@formcontrolname="name"]'
    INPUT_WEIGHT_EXACT = '//input[@type="number" and @formcontrolname="value"]'
    SELECT_WEIGHT_CATEGORY = '//div[@class="mat-select-arrow-wrapper ng-tns-c60-5"]'
    TEXT_UP_TO_0_15 = '//span[text()=" до 0,15 кг "]'
    INPUT_REGISTRATION_NUMBER = '//input[@formcontrolname = "aircraftIdentification"]'
    INPUT_PILOT_LICENCE = '//input[@formcontrolname = "remotePilotLicence"]'
    INPUT_MODEL_BVS = '//input[@class="mat-input-element border-0 position-absolute ng-untouched ng-pristine ng-valid"]'
    INPUT_OPR = '//input[@formcontrolname = "opr"]'
    TEXT_NOT_FOUND = '//span[text()=" Не найдено "]'
    INPUT_MAX_FLIGHT_TIME = '//input[@data-testid="alsTimeInputElement"]'
    INPUT_MAX_FLIGHT_RANGE_VALUE = '//input[@class="mat-input-element mat-form-field-autofill-control ng-tns-c49-10 ng-untouched ng-pristine ng-valid cdk-text-field-autofill-monitored"]'
    BUTTON_MAX_FLIGHT_RANGE_UNIT = '//div[@class="mat-form-field-suffix ng-tns-c49-10 ng-star-inserted"]//button'
    TEXT_M = '//button[text()=" М "]'
    INPUT_LEVEL_1_VALUE = '//label[@class="mat-form-field-label ng-tns-c49-11 mat-empty mat-form-field-empty ng-star-inserted"]'
    BUTTON_LEVEL_1_UNIT = '//div[@class="mat-form-field-suffix ng-tns-c49-11 ng-star-inserted"]//button'
    TEXT_M_QNE = '//button[text()=" M/QNE "]'
    INPUT_LEVEL_2_VALUE = '//label[@class="mat-form-field-label ng-tns-c49-12 mat-empty mat-form-field-empty ng-star-inserted"]'
    BUTTON_LEVEL_2_UNIT = '//div[@class="mat-form-field-suffix ng-tns-c49-12 ng-star-inserted"]//button'
    TEXT_M_AMSL = '//button[text()=" M/AMSL "]'
    BUTTON_SAVE = '//button[@class="mat-focus-indicator w-100 mat-stroked-button mat-button-base mat-primary ng-star-inserted" and @title="Сохранить"]'
    POP_UP_SAVE_BLA = 'BLA создан'
    BLA_IN_LIST = f'//div[@class="text-truncate ng-star-inserted" and @title="{BLA_NAME}"]'

    def go_create_bla_page(self):
        self.page.goto(f'{self.base_url}/aircraft/bla/bla/create')
        expect(self.page).to_have_title('СППИ - Воздушные суда - БВС - Добавить')
        return self

    def input_form_up_to_0_15_kg(self):

        self.input_value_by_letter(self.INPUT_NAME, self.BLA_NAME)
        self.input_value_by_letter(self.INPUT_WEIGHT_EXACT, '0.1')
        self.page.wait_for_selector(self.SELECT_WEIGHT_CATEGORY).click()
        self.page.wait_for_selector(self.TEXT_UP_TO_0_15).click()
        self.input_value_by_letter(self.INPUT_REGISTRATION_NUMBER, '11111')
        self.input_value_by_letter(self.INPUT_PILOT_LICENCE, 'N33')
        self.page.wait_for_selector(self.INPUT_MODEL_BVS).fill('DJI-SUPERB')
        self.page.locator(self.TEXT_NOT_FOUND).blur()
        self.input_value_by_letter(self.INPUT_OPR, 'AEROBAZA')
        self.input_value_by_letter(self.INPUT_MAX_FLIGHT_TIME, '0056')
        self.page.wait_for_selector(self.INPUT_MAX_FLIGHT_RANGE_VALUE).fill('100')
        self.page.wait_for_selector(self.BUTTON_MAX_FLIGHT_RANGE_UNIT).click()
        self.page.wait_for_selector(self.TEXT_M).click()
        self.page.wait_for_selector(self.INPUT_LEVEL_1_VALUE).fill('100')
        self.page.wait_for_selector(self.BUTTON_LEVEL_1_UNIT).click()
        self.page.wait_for_selector(self.TEXT_M_QNE).click()
        self.page.wait_for_selector(self.INPUT_LEVEL_2_VALUE).fill('200')
        self.page.wait_for_selector(self.BUTTON_LEVEL_2_UNIT).click()
        self.page.wait_for_selector(self.TEXT_M_AMSL).click()
        return self

    def click_save_button(self):
        self.page.wait_for_selector(self.BUTTON_SAVE).click()
        expect(self.page.get_by_text(self.POP_UP_SAVE_BLA)).to_be_visible()
        expect(self.page).to_have_title('СППИ - Воздушные суда - БВС - Список')
        return self

    def check_created_bla(self):
        expect(self.page.locator(self.BLA_IN_LIST)).to_be_visible()

    # def delete_created_bla(self):
