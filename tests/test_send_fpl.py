import allure
from page_objects.fpl_page import FplPage
from playwright.sync_api import expect
from utils.pw_helpers import FlightRules, FlightType, TurbulenceCat, Unit, FplType


class TestSendFpl:
    @allure.feature('FPL')
    def test_send_fpl_utp_ad_route_from_form(self, pilot_page):
        fpl = FplPage(pilot_page)
        fpl.go_create_fpl_page()
        fpl.close_confirm_modal()
        fpl.choose_fpl_type(FplType.utp_ad())
        fpl.fill_reg_number('04927')
        fpl.choose_flight_rules(FlightRules.i()).choose_flight_type((FlightType.x()))
        fpl.fill_aircraft_type('MI8')
        fpl.choose_turbulence_cat(TurbulenceCat.m()).fill_equipment('ADE3T/HB2')
        fpl.fill_aerodrome_dep('XUBW').input_desc_time.clear()
        fpl.fill_desc_time('04', '00')
        fpl.choose_level_unit(Unit.m_amsl()).fill_level_value('4500')
        fpl.button_specify_route.click()
        fpl.ok_button_in_information_modal.click()
        fpl.fill_route('XUMH DCT UUMU')
        fpl.fill_aerodrome_arr('UUMC').fill_duration('00', '50')
        fpl.button_submit.dblclick()
        fpl.modal_diagnostic.is_visible()
        expect(fpl.text_fpl_in_diagnostic_modal).to_contain_text(
            'FPL-04927-IX -MI8/M-ADE3T/HB2 -XUBW0400 -/RA/M0450 XUMH DCT UUMU -UUMC0050')
        fpl.button_send_fpl.click()
        fpl.modal_sent_success.is_visible()

    @allure.feature('FPL')
    def test_send_fpl_utp_ad_without_route_from_form(self, pilot_page):
        fpl = FplPage(pilot_page)
        fpl.go_create_fpl_page()
        fpl.close_confirm_modal()
        fpl.choose_fpl_type(FplType.utp_ad())
        fpl.fill_reg_number('04927')
        fpl.choose_flight_rules(FlightRules.i()).choose_flight_type((FlightType.x()))
        fpl.fill_aircraft_type('MI8')
        fpl.choose_turbulence_cat(TurbulenceCat.m()).fill_equipment('ADE3T/HB2')
        fpl.fill_aerodrome_dep('UUBW').input_desc_time.clear()
        fpl.fill_desc_time('04', '00')
        fpl.choose_level_unit(Unit.m_amsl()).fill_level_value('4500')
        fpl.fill_aerodrome_arr('UUBW').fill_duration('00', '20')
        fpl.button_submit.dblclick()
        fpl.modal_diagnostic.is_visible()
        expect(fpl.text_fpl_in_diagnostic_modal).to_contain_text(
            'FPL-04927-IX -MI8/M-ADE3T/HB2 -UUBW0400 -/RA/M0450 -UUBW0020')
        fpl.button_send_fpl.click()
        fpl.modal_sent_success.is_visible()
