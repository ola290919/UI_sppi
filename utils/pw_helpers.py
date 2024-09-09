import random
import string

import allure
from playwright.sync_api import expect, Locator


def random_string(lenght=10):
    return "".join([random.choice(string.ascii_letters) for _ in range(lenght)])


@allure.step("Заполнить поле {locator} значением {value}")
def fill_and_check_value(locator: Locator, value: str):
    locator.fill(value)
    expect(locator).to_have_value(value)


@allure.step("Заполнить временное поле {locator} значением {hh}:{mm}")
def fill_and_check_value_time(locator, hh: str, mm: str):
    locator.fill(hh + mm)
    expect(locator).to_have_value(hh + ':' + mm)

class Weight:

    def up_to_0_15():
        return 'до 0,15 кг'

    def from_0_15_up_to_30():
        return 'от 0,15 до 30 кг'

    def more_than_30():
        return 'более 30 кг'


class Unit:
    def m_qne():
        return 'M/QNE'

    def m_amsl():
        return 'M/AMSL'

    def fl():
        return 'FL'

    def ft_agl():
        return 'FT/AGL'

    def tabel():
        return 'ТАБЕЛЬ'

    def m():
        return 'М'

    def km():
        return 'КМ'

    def nm():
        return 'NM'


class FlightRules:
    def i():
        return 'I ППП'

    def v():
        return 'V ПВП'

    def y():
        return 'Y ППП/ПВП'

    def z():
        return 'Z ПВП/ППП'


class FlightType:
    def s():
        return 'S по расписанию'

    def n():
        return 'N вне расписания'

    def g():
        return 'G АОН'

    def m():
        return 'M гос. авиация'

    def x():
        return 'X прочее'


class TurbulenceCat:
    def h():
        return 'H от 136000 до 500000 кг'

    def j():
        return 'J A-380-800'

    def m():
        return 'M от 7000 до 136000 кг'

    def l():
        return 'L до 7000 кг'


class FplType:
    def vs_flight():
        return 'Полёт воздушного судна'

    def utp_ad():
        return 'УТП в районе аэродрома'

    def utp_area():
        return 'УТП с площадок'


class FlightStatus:
    def sent():
        return 'На обработке'

    def ack():
        return 'Принят'

    def rej():
        return 'Отвергнут'

    def cnl():
        return 'Отменен'

    def dep():
        return 'В полёте'

    def arr():
        return 'Выполнен'
