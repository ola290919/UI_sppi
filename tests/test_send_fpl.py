import allure
from helpers import FlightRules, FlightType, TurbulenceCat, Unit, FplType
from page_objects.auth_page import As
from page_objects.fpl_page import FplPage
from playwright.sync_api import expect


class TestSendFpl:
    @allure.feature('')
    def test_send_fpl_utp_ad_route_from_form(self, auth):
        fpl = FplPage(auth(As.PILOT))
        fpl.go_create_fpl_page()
        fpl.close_confirm_modal()
        fpl.choose_fpl_type(FplType.utp_ad())
        fpl.input_reg_number.press_sequentially('04927')
        fpl.choose_flight_rules(FlightRules.i()).choose_flight_type((FlightType.x()))
        fpl.fill_aircraft_type('MI8')
        fpl.choose_turbulence_cat(TurbulenceCat.m()).input_equipment.fill('ADE3T/HB2')
        fpl.fill_aerodrome_dep('XUBW').input_desc_time.clear()
        fpl.input_desc_time.fill('0400')
        fpl.choose_level_unit(Unit.m_amsl()).input_level_value.fill('4500')
        fpl.button_specify_route.click()
        fpl.ok_button_in_information_modal.click()
        fpl.textarea_route.press_sequentially('XUMH DCT UUMU')
        fpl.fill_aerodrome_arr('UUMC').input_duration.fill('0050')
        fpl.button_submit.dblclick()
        fpl.modal_diagnostic.is_visible()
        expect(fpl.text_fpl_in_diagnostic_modal).to_contain_text(
            'FPL-04927-IX -MI8/M-ADE3T/HB2 -XUBW0400 -/RA/M0450 XUMH DCT UUMU -UUMC0050')
        fpl.button_send_fpl.click()
        fpl.modal_sent_success.is_visible()

    def test_send_fpl_utp_ad_without_route_from_form(self, auth):
        fpl = FplPage(auth(As.PILOT))
        fpl.go_create_fpl_page()
        fpl.close_confirm_modal()
        fpl.choose_fpl_type(FplType.utp_ad())
        fpl.input_reg_number.press_sequentially('04927')
        fpl.choose_flight_rules(FlightRules.i()).choose_flight_type((FlightType.x()))
        fpl.fill_aircraft_type('MI8')
        fpl.choose_turbulence_cat(TurbulenceCat.m()).input_equipment.fill('ADE3T/HB2')
        fpl.fill_aerodrome_dep('UUBW').input_desc_time.clear()
        fpl.input_desc_time.press_sequentially('0400')
        fpl.choose_level_unit(Unit.m_amsl()).input_level_value.fill('4500')
        fpl.fill_aerodrome_arr('UUBW').input_duration.fill('0020')
        fpl.button_submit.dblclick()
        fpl.modal_diagnostic.is_visible()
        expect(fpl.text_fpl_in_diagnostic_modal).to_contain_text(
            'FPL-04927-IX -MI8/M-ADE3T/HB2 -UUBW0400 -/RA/M0450 -UUBW0020')
        fpl.button_send_fpl.click()
        fpl.modal_sent_success.is_visible()
