import allure
from page_objects.bla_page import BlaPage
from utils.pw_helpers import random_string, Weight, Unit


class TestCreateBla:

    @allure.feature('BLA')
    def test_bla_up_to_0_15(self, pilot_page):
        bla = BlaPage(pilot_page)
        bla_name = random_string() + ' Test light'
        bla.go_create_bla_page()
        bla.fill_name(bla_name)
        bla.choose_weight_category(Weight.up_to_0_15()).fill_weight_exact('0.1')
        bla.fill_aircraft_identification('11111')
        bla.fill_pilot_licence('N33')
        bla.fill_model_bvs('DJI-SUPERB')
        bla.field_text_not_found.blur()
        bla.fill_opr('AEROBAZA')
        bla.fill_max_flight_time('00', '56')
        bla.choose_max_flight_range_unit(Unit.m()).fill_max_flight_range_value('100')
        bla.choose_level_1_unit(Unit.m_qne()).fill_level_1_value('100')
        bla.choose_level_2_unit(Unit.m_amsl()).fill_level_2_value('200')
        bla.click_save_button().check_title_grid_page().check_created_bla(bla_name)

    @allure.feature('BLA')
    def test_create_bla_from_0_15_up_to_30(self, pilot_page):
        bla = BlaPage(pilot_page)
        bla_name = random_string() + ' Test medium'
        bla.go_create_bla_page()
        bla.fill_name(bla_name)
        bla.choose_weight_category(Weight.from_0_15_up_to_30()).fill_weight_exact('6')
        bla.fill_registration_number('4444444')
        bla.fill_serial_number('555')
        bla.fill_pilot_licence('N55')
        bla.fill_model_bvs('DJI-MEDIUM')
        bla.field_text_not_found.blur()
        bla.fill_max_flight_time('05', '00')
        bla.choose_max_flight_range_unit(Unit.km()).fill_max_flight_range_value('99')
        bla.choose_level_1_unit(Unit.m_amsl()).fill_level_1_value('100')
        bla.choose_level_2_unit(Unit.m_amsl()).fill_level_2_value('200')
        bla.click_save_button().check_title_grid_page().check_created_bla(bla_name)

    @allure.feature('BLA')
    def test_bla_more_than_30(self, pilot_page):
        bla = BlaPage(pilot_page)
        bla_name = random_string() + ' Test heavy'
        bla.go_create_bla_page()
        bla.fill_name(bla_name)
        bla.choose_weight_category(Weight.more_than_30()).fill_weight_exact('32')
        bla.fill_aircraft_identification('22222')
        bla.fill_pilot_licence('N44')
        bla.fill_model_bvs('DJI-HEAVY')
        bla.field_text_not_found.blur()
        bla.fill_max_flight_time('01', '00')
        bla.choose_max_flight_range_unit(Unit.nm()).fill_max_flight_range_value('54')
        bla.choose_level_1_unit(Unit.m_qne()).fill_level_1_value('100')
        bla.choose_level_2_unit(Unit.m_qne()).fill_level_2_value('200')
        bla.click_save_button().check_title_grid_page().check_created_bla(bla_name)
