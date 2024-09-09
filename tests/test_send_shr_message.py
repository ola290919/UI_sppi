import allure
from utils.pw_helpers import FlightRules, FlightType, TurbulenceCat, Unit, FplType, FlightStatus
from utils.sppi_auth_client import As
from page_objects.shr_message_page import ShrMessagePage
from playwright.sync_api import expect
import time


class TestSendShrMessage:
    @allure.feature('')
    def test_send_ack(self, auth, name_of_sent_shr):
        mes = ShrMessagePage(auth(As.ATM_DISPATCHER_MOSCOW))
        mes.go_shr_grid_page()
        mes.check_flight_status(name_of_sent_shr, FlightStatus.sent())
        mes.open_context_menu(name_of_sent_shr)
        mes.ack_button_click()
        mes.send_ack()
        mes.check_flight_status(name_of_sent_shr, FlightStatus.ack())

    def test_send_rej_for_sent_shr(self, auth, name_of_sent_shr):
        mes = ShrMessagePage(auth(As.ATM_DISPATCHER_MOSCOW))
        mes.go_shr_grid_page()
        mes.check_flight_status(name_of_sent_shr, FlightStatus.sent())
        mes.open_context_menu(name_of_sent_shr)
        mes.rej_button_click()
        mes.send_rej()
        mes.check_flight_status(name_of_sent_shr, FlightStatus.rej())

    def test_send_rej_for_ack_shr(self, auth, name_of_ack_shr):
        mes = ShrMessagePage(auth(As.ATM_DISPATCHER_MOSCOW))
        mes.go_shr_grid_page()
        mes.check_flight_status(name_of_ack_shr, FlightStatus.ack())
        mes.open_context_menu(name_of_ack_shr)
        mes.rej_button_click()
        mes.send_rej()
        mes.check_flight_status(name_of_ack_shr, FlightStatus.rej())

    def test_send_cnl_for_sent_shr(self, auth, name_of_sent_shr):
        mes = ShrMessagePage(auth(As.PILOT))
        mes.go_shr_grid_page()
        mes.check_flight_status(name_of_sent_shr, FlightStatus.sent())
        mes.open_context_menu(name_of_sent_shr)
        mes.cnl_button_click()
        mes.send_cnl()
        mes.check_flight_status(name_of_sent_shr, FlightStatus.cnl())

    def test_send_cnl_for_ack_shr(self, auth, name_of_ack_shr):
        mes = ShrMessagePage(auth(As.PILOT))
        mes.go_shr_grid_page()
        mes.check_flight_status(name_of_ack_shr, FlightStatus.ack())
        mes.open_context_menu(name_of_ack_shr)
        mes.cnl_button_click()
        mes.send_cnl()
        mes.check_flight_status(name_of_ack_shr, FlightStatus.cnl())

    def test_send_dep_for_ack_shr(self, auth, name_of_ack_shr):
        mes = ShrMessagePage(auth(As.PILOT))
        mes.go_shr_grid_page()
        mes.check_flight_status(name_of_ack_shr, FlightStatus.ack())
        mes.open_context_menu(name_of_ack_shr)
        mes.dep_button_click()
        mes.send_dep()
        mes.check_flight_status(name_of_ack_shr, FlightStatus.dep())

    def test_send_arr_for_dep_shr(self, auth, name_of_dep_shr):
        mes = ShrMessagePage(auth(As.PILOT))
        mes.go_shr_grid_page()
        mes.check_flight_status(name_of_dep_shr, FlightStatus.dep())
        mes.open_context_menu(name_of_dep_shr)
        mes.arr_button_click()
        mes.send_arr()
        mes.check_flight_status(name_of_dep_shr, FlightStatus.arr())
