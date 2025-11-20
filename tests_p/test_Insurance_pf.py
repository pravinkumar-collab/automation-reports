import time
import pytest
from pages.InsurancePage import InsurancePage
from pages.LoginPage import LoginPage
from pages.NomineePage import NomineePage
from pages.PanDetailsPage import PanDetailsPage
from pages.PaymentOptionsPage import PaymentOptionsPage
from pages.PersonalDetailsPage import PersonalDetailsPage
from pages.ReviewDetailsPage import ReviewDetailsPage
from pages.SuperappPage import SuperappPage
from ParentTest import ParentTest
from utilities.config_reader import get_config

@pytest.mark.runonly
class TestInsurance(ParentTest):

    def test_login(self):
        login_page = LoginPage(self.driver)
        login_page.perform_full_login("8828060180","123456")

    def test_register_yourself(self):
        pdp = PersonalDetailsPage(self.driver)
        pdp.enter_personal_details("Pravin","P","pravin.kumar@fatakpay.com",'400063')
        self.super_app = SuperappPage(self.driver)
        self.super_app.home_is_displayed()

    def test_select_insurance_menu(self):
        self.super_app = SuperappPage(self.driver)
        self.super_app.click_on_insurance_section()

    def test_select_insurance_type(self):
        insurance_page = InsurancePage(self.driver)
        insurance_page.begin_product("cancer")

    def test_register_pan_details(self):
        pan_detail_page = PanDetailsPage(self.driver)
        pan_detail_page.select_dob("12.03.2002")
        pan_details = get_config("basic details","pan")
        pan_detail_page.complete_pan_details(pan_details,"Male")

    def test_register_nominee_details(self):
        nominee_page = NomineePage(self.driver)
        nominee_page.complete_nominee_details("Test","23","Father","7788990066")

    def test_review_insurance_details(self):
        review_detail_page = ReviewDetailsPage(self.driver)
        review_detail_page.verify_display_of_amount_field()
        review_detail_page.click_on_proceed_button()
        time.sleep(20)

    def test_complete_payment(self):
        pop = PaymentOptionsPage(self.driver)
        pop.select_payment()
        time.sleep(10)
        congrats_msg = pop.verify_congratulation_text()
        assert "Your policy number will be generated against this " in congrats_msg
        print("Working")