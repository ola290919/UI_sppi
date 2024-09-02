"""
Тесты проверки сценариев
"""

import allure
from helpers import (random_string, category_up_to_0_15, category_from_0_15_up_to_30, level_unit_m_qne,
                     level_unit_m_amsl, flight_range_unit_m,
                     flight_range_unit_km)
from page_objects.auth_page import As
from page_objects.bla_page import BlaPage


class TestBlaCreate():
    @allure.feature('')
    def test_bla_up_to_0_15(self, auth):
        bla = BlaPage(auth(As.PILOT))
        bla_name = random_string()
        bla.go_create_bla_page()
        bla.input_name.press_sequentially(bla_name)
        bla.input_weight_exact.fill('0.1')
        bla.choose_weight_category(category_up_to_0_15())
        bla.aircraft_identification.fill('11111')
        bla.pilot_licence.fill('N33')
        bla.model_bvs.fill('DJI-SUPERB')
        bla.field_text_not_found.blur()
        bla.opr.fill('AEROBAZA')
        bla.max_flight_time.fill('0056')
        bla.choose_max_flight_range_unit(flight_range_unit_m()).max_flight_range_value.fill('100')
        bla.choose_level_1_unit(level_unit_m_qne()).level_1_value.fill('100')
        bla.choose_level_2_unit(level_unit_m_amsl()).level_2_value.fill('200')
        bla.click_save_button().check_title_grid_page().check_created_bla(bla_name)

    def test_create_bla_from_0_15_up_to_30(self, auth):
        bla = BlaPage(auth(As.PILOT))
        bla_name = random_string()
        bla.go_create_bla_page()
        bla.input_name.press_sequentially(bla_name)
        bla.input_weight_exact.fill('6')
        bla.choose_weight_category(category_from_0_15_up_to_30())
        bla.registration_number.fill('4444444')
        bla.serial_number.fill('555')
        bla.pilot_licence.fill('N55')
        bla.model_bvs.fill('DJI-MEDIUM')
        bla.field_text_not_found.blur()
        bla.max_flight_time.fill('0500')
        bla.choose_max_flight_range_unit(flight_range_unit_km()).max_flight_range_value.fill('99')
        bla.choose_level_1_unit(level_unit_m_amsl()).level_1_value.fill('100')
        bla.choose_level_2_unit(level_unit_m_qne()).level_2_value.fill('200')
        bla.click_save_button().check_title_grid_page().check_created_bla(bla_name)

    def test_bla_more_than_30(self, auth):
        pass
