from pages.ParentPage import ParentPage
from pages.otpPage import OtpPage
from utilities.captcha import solve_captcha


class LoginPage(ParentPage):
    def __init__(self,driver):
        super().__init__(driver)

    phone_number_id = "mat-input-0"
    captcha_id = "mat-input-1"
    captcha_refresh_css = "span.material-icons-outlined.cursor-pointer"
    send_otp_css = "span.mat-mdc-button-touch-target"
    deny_popUP_xpath= "//button[contains(text(),'do this later')]"
    captcha_image_css = "captcha_width ng-star-inserted"
    popUP_section_id = "webpush-prompt"
    phoneNumber_warning_xpath = "//mat-error[contains(@class,'mat-mdc-form-field-error ')]"
    captcha_warning_xpath = "//mat-error[normalize-space()='Captcha is required']"


    def enter_phone_number(self,text):
        self.type_into_element("phone_number_id",self.phone_number_id,text)

    def enter_captcha_code(self,text):
        self.type_into_element("captcha_id",self.captcha_id,text)

    def click_on_refresh(self):
        self.click_on_element(  "captcha_refresh_css",self.captcha_refresh_css)

    def click_on_otp(self):
        self.wait_for_element("send_otp_css",self.send_otp_css,condition="clickable")
        self.click_on_element("send_otp_css",self.send_otp_css,condition="clickable",scroll=True)
        return OtpPage(self.driver)

    def deny_push_notification(self):
        '''iframe_id = "webpush-prompt"
        deny_xpath = self.deny_popUP_xpath

        # STEP 1 — Wait up to 12 seconds for iframe to appear and switch
        end_time = time.time() + 12
        while time.time() < end_time:
            try:
                self.driver.switch_to.frame(iframe_id)
                break
            except:
                time.sleep(0.2)
        else:
            return  # iframe never appeared → safe exit

        # STEP 2 — Inside iframe → wait for deny button by XPATH
        try:
            end_time = time.time() + 10
            while time.time() < end_time:
                try:
                    btn = self.driver.find_element(By.XPATH, deny_xpath)
                    if btn.is_displayed():
                        btn.click()
                        break
                except:
                    pass
                time.sleep(0.2)
        finally:
            # STEP 3 — Always go back to main DOM
            self.driver.switch_to.default_content()
        '''
        # self.wait_for_element("popUP_section_id",self.popUP_section_id,condition="presence")
        self.switch_to_frame("webpush-bubble")
        self.wait_for_element("deny_popUP_xpath", self.deny_popUP_xpath, condition="clickable")
        self.click_on_element("deny_popUP_xpath", self.deny_popUP_xpath, scroll=True)
        self.switch_to_default_content()

    def captcha_is_displayed(self):
        # self.wait_for_element("captcha_image_css",self.captcha_image_css,condition = "visible")
        self.get_element("captcha_image_css",self.captcha_image_css,condition = "displayed")

    def perform_full_login(self,phone,otp_text):
        # self.captcha_is_displayed()
        self.deny_push_notification()
        self.enter_phone_number(phone)
        captcha_text = solve_captcha(self.driver)
        if captcha_text:
            self.enter_captcha_code(captcha_text)
            print(f"Captcha auto-filled: {captcha_text}")
        else:
            print("Captcha couldn't be filled")
        self.click_on_otp()
        otp_page = OtpPage(self.driver)
        otp_page.enter_otp(otp_text)
        otp_page.click_on_verify_otp()

    def mandatory_login_fields_warning(self):
        self.click_on_element("phone_number_id",self.phone_number_id)
        self.wait_for_stability()
        self.click_on_element("_tag","body")
        phone_warning =  self.get_message("phoneNumber_warning_xpath",self.phoneNumber_warning_xpath)

        self.click_on_element("captcha_id",self.captcha_id)
        self.wait_for_stability()
        self.click_on_element("_tag","body")
        captcha_warning = self.get_message("captcha_warning_xpath",self.captcha_warning_xpath)

        return  phone_warning, captcha_warning



