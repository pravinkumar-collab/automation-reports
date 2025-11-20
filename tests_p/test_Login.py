from pages.LoginPage import LoginPage
from ParentTest import ParentTest


class TestLogin(ParentTest):
    def test_login(self):
        login_page  = LoginPage(self.driver)
        login_page.perform_full_login("8828060180","123456")
        ''' otp_page = OtpPage(self.driver)
        # otp_page.enter_otp()
        otp_page.enter_otp()
        otp_page.click_on_verify_otp()
        '''
