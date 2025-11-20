from pages.ParentPage import ParentPage


class OtpPage(ParentPage):

    def __init__(self,driver):
        super().__init__(driver)

    otp_field_xpath = "//input[@aria-label='a']"
    verify_otp_css = "span.ng-star-inserted"


    def enter_otp(self,otp_text):
        # self.type_into_element("otp_field_xpath",self.otp_field_xpath,otp_text)
        self.get_element("otp_field_xpath",self.otp_field_xpath,condition="visible")
        self.type_into_element("otp_field_xpath",self.otp_field_xpath,otp_text)



    def click_on_verify_otp(self):
        self.click_on_element("verify_otp_css",self.verify_otp_css)