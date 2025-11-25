import time
import pytest

from ParentTest import ParentTest
from pages.InsurancePage import InsurancePage
from pages.LoginPage import LoginPage
from pages.NomineePage import NomineePage
from pages.PanDetailsPage import PanDetailsPage
from pages.PaymentOptionsPage import PaymentOptionsPage
from pages.PersonalDetailsPage import PersonalDetailsPage
from pages.ReviewDetailsPage import ReviewDetailsPage
from pages.SuperappPage import SuperappPage

from utilities.config_reader import get_config


@pytest.mark.run
class TestInsuranceNegative(ParentTest):

    def test_mandatory_login_fields(self):
        self.login_page = LoginPage(self.driver)
        phone_msg, captcha_msg = self.login_page.mandatory_login_fields_warning()
        assert phone_msg.strip() == "Phone number is required"
        assert captcha_msg.strip() == "Captcha is required"

    def test_mandatory_fields_positive(self):
        self.login_page = LoginPage(self.driver)
        self.login_page.perform_full_login("8828060180","123456")

    def test_mandatory_register_yourself_negative(self):
        pdp = PersonalDetailsPage(self.driver)
        firstname_msg, lastname_msg, email_msg, pincode_msg = pdp.mandatory_register_yourself_warning()
        assert firstname_msg.strip() == "First Name is required"
        assert lastname_msg.strip() == "Last Name is required"
        assert email_msg.strip() == "Email is required"
        assert pincode_msg.strip() == "Pincode is required"

    def test_mandatory_register_yourself_positive(self):
        pdp = PersonalDetailsPage(self.driver)
        pdp.enter_personal_details("Pravin", "P", "pravin.kumar@fatakpay.com", '400063')
        self.super_app = SuperappPage(self.driver)
        self.super_app.home_is_displayed()

    def test_select_insurance_menu(self):
        self.super_app = SuperappPage(self.driver)
        self.super_app.click_on_insurance_section()

    def test_select_insurance_type(self):
        insurance_page = InsurancePage(self.driver)
        insurance_page.begin_product("cancer")

    def test_mandatory_pan_details_negative(self):
        self.pan_details_page = PanDetailsPage(self.driver)
        dob_msg, pan_msg = self.pan_details_page.mandatory_pan_details_warning()
        print(dob_msg)
        assert dob_msg.strip() == "Please input your birth date!"
        assert pan_msg.strip() == "PAN Number is required"

    def test_mandatory_pan_details_positive(self):
        pan_detail_page = PanDetailsPage(self.driver)
        pan_detail_page.select_dob("12.03.2002")
        pan_details = get_config("basic details", "pan")
        pan_detail_page.complete_pan_details(pan_details, "Male")

    def test_mandatory_nominee_details_negative(self):
        nominee_page = NomineePage(self.driver)
        nominee_name_msg, nominee_age_msg, nominee_relation_msg, nominee_mobile_msg = nominee_page.mandatory_nominee_details_warning()
        assert nominee_name_msg.strip() == "Full Name is required"
        assert nominee_age_msg.strip() == "Valid Nominee age must be between 18 to 110!"
        assert nominee_relation_msg.strip() == "Please select your Relationship !"
        assert nominee_mobile_msg.strip() == "Phone number is required"

    def test_mandatory_nominee_details_positive(self):
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





