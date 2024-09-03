import allure
from helpers import random_string, Weight, Unit
from page_objects.auth_page import As
from page_objects.bla_page import BlaPage


class TestCreateBla:
    @allure.feature('')
    def test_bla_up_to_0_15(self, auth):
        bla = BlaPage(auth(As.PILOT))
        bla_name = random_string()
        bla.go_create_bla_page()
        bla.input_name.press_sequentially(bla_name)
        bla.input_weight_exact.fill('0.1')
        bla.choose_weight_category(Weight.up_to_0_15())
        bla.input_aircraft_identification.fill('11111')
        bla.input_pilot_licence.fill('N33')
        bla.input_model_bvs.fill('DJI-SUPERB')
        bla.field_text_not_found.blur()
        bla.input_opr.fill('AEROBAZA')
        bla.input_max_flight_time.fill('0056')
        bla.choose_max_flight_range_unit(Unit.m()).input_max_flight_range_value.fill('100')
        bla.choose_level_1_unit(Unit.m_qne()).input_level_1_value.fill('100')
        bla.choose_level_2_unit(Unit.m_amsl()).input_level_2_value.fill('200')
        bla.click_save_button().check_title_grid_page().check_created_bla(bla_name)

    def test_create_bla_from_0_15_up_to_30(self, auth):
        bla = BlaPage(auth(As.PILOT))
        bla_name = random_string()
        bla.go_create_bla_page()
        bla.input_name.press_sequentially(bla_name)
        bla.input_weight_exact.fill('6')
        bla.choose_weight_category(Weight.from_0_15_up_to_30())
        bla.input_registration_number.fill('4444444')
        bla.input_serial_number.fill('555')
        bla.input_pilot_licence.fill('N55')
        bla.input_model_bvs.fill('DJI-MEDIUM')
        bla.field_text_not_found.blur()
        bla.input_max_flight_time.fill('0500')
        bla.choose_max_flight_range_unit(Unit.km()).input_max_flight_range_value.fill('99')
        bla.choose_level_1_unit(Unit.m_amsl()).input_level_1_value.fill('100')
        bla.choose_level_2_unit(Unit.m_amsl()).input_level_2_value.fill('200')
        bla.click_save_button().check_title_grid_page().check_created_bla(bla_name)

    def test_bla_more_than_30(self, auth):
        bla = BlaPage(auth(As.PILOT))
        bla_name = random_string()
        bla.go_create_bla_page()
        bla.input_name.press_sequentially(bla_name)
        bla.input_weight_exact.fill('32')
        bla.choose_weight_category(Weight.more_than_30())
        bla.input_aircraft_identification.fill('22222')
        bla.input_pilot_licence.fill('N44')
        bla.input_model_bvs.fill('DJI-HEAVY')
        bla.field_text_not_found.blur()
        bla.input_max_flight_time.fill('0100')
        bla.choose_max_flight_range_unit(Unit.nm()).input_max_flight_range_value.fill('54')
        bla.choose_level_1_unit(Unit.m_qne()).input_level_1_value.fill('100')
        bla.choose_level_2_unit(Unit.m_qne()).input_level_2_value.fill('200')
        bla.click_save_button().check_title_grid_page().check_created_bla(bla_name)
