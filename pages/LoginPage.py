from pages.ParentPage import ParentPage
from pages.otpPage import OtpPage
from utilities.captcha import solve_captcha


class LoginPage(ParentPage):
    def __init__(self, driver):
        super().__init__(driver)

    phone_number_id = "mat-input-0"
    captcha_id = "mat-input-1"
    captcha_refresh_xpath = "//span[@class='material-icons-outlined cursor-pointer']"
    send_otp_css = "span.mat-mdc-button-touch-target"
    deny_popUP_xpath = "//button[contains(text(),'do this later')]"
    captcha_image_xpath = "//img[@alt='Captcha']"
    popUP_section_id = "webpush-bubble"
    phoneNumber_warning_xpath = "//mat-error[contains(@class,'mat-mdc-form-field-error ')]"
    captcha_warning_xpath = "//mat-error[normalize-space()='Captcha is required']"

    def enter_phone_number(self, text):
        self.type_into_element("phone_number_id", self.phone_number_id, text)

    def enter_captcha_code(self, text):
        self.type_into_element("captcha_id", self.captcha_id, text)

    def click_on_otp(self):
        self.wait_for_element("send_otp_css", self.send_otp_css, condition="clickable")
        self.click_on_element("send_otp_css", self.send_otp_css, condition="clickable", scroll=True)
        return OtpPage(self.driver)

    def deny_push_notification(self):
        try:
            self.wait_for_element("popUP_section_id", self.popUP_section_id, condition="frame", timeout=2)
        except:
            return
        try:
            self.wait_for_element("deny_popUP_xpath", self.deny_popUP_xpath, condition="clickable", timeout=2)
            self.click_on_element("deny_popUP_xpath", self.deny_popUP_xpath, scroll=True, timeout=2)
            print("[INFO] Push notification dismissed.")
        except:
            print("[INFO] Frame shown,but deny button not available")
        finally:
            self.switch_to_default_content()

    def wait_for_valid_captcha(self, max_attempts=5):
        for attempt in range(max_attempts):
            captcha = self.get_element("captcha_image_xpath", self.captcha_image_xpath, condition="displayed")
            is_loaded = self.driver.execute_script("""
        let img = arguments[0];
        return img && img.complete && img.naturalWidth > 0 && img.naturalHeight > 0;
        """, captcha)
            if is_loaded:
                print(f"CAPTCHA loaded properly on attempt: {attempt + 1}")
                return captcha

            print(f"CAPTCHA not loaded, refreshing (attempt: {attempt + 1})")
            self.click_on_element("captcha_refresh_xpath", self.captcha_refresh_xpath)
            self.wait_for_stability()
        raise Exception("CAPTCHA failed to load after multiple attempts.")

    def perform_full_login(self, phone, otp_text):
        self.deny_push_notification()
        self.enter_phone_number(phone)
        self.deny_push_notification()
        self.wait_for_valid_captcha()
        captcha_text = solve_captcha(self.driver)
        if captcha_text:
            self.enter_captcha_code(captcha_text)
            print(f"Captcha auto-filled: {captcha_text}")
        else:
            print("Captcha couldn't be filled")
        self.deny_push_notification()
        self.click_on_otp()
        otp_page = OtpPage(self.driver)
        otp_page.enter_otp(otp_text)
        otp_page.click_on_verify_otp()
        self.deny_push_notification()

    def mandatory_login_fields_warning(self):
        self.click_on_element("phone_number_id", self.phone_number_id)
        self.wait_for_stability()
        self.click_on_element("_tag", "body")
        phone_warning = self.get_message("phoneNumber_warning_xpath", self.phoneNumber_warning_xpath)

        self.click_on_element("captcha_id", self.captcha_id)
        self.wait_for_stability()
        self.click_on_element("_tag", "body")
        captcha_warning = self.get_message("captcha_warning_xpath", self.captcha_warning_xpath)

        return phone_warning, captcha_warning
