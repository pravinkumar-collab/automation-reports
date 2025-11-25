from pages.ParentPage import ParentPage


class PaymentOptionsPage(ParentPage):

    def __init__(self,driver):
        super().__init__(driver)

    razor_pay_frame_xpath = "//iframe[contains(@src, 'razorpay.com/v1/checkout/public')]"
    show_qr_xpath = "//span[@name='generateQR']"
    continue_and_pay_xpath = "//button[normalize-space()='Continue & Pay']"
    congratulations_xpath = "//p[contains(text(),'Your policy number will be generated against this ')]"

    def switch_to_payment_window(self):
        for attempt in range(3):
            try:
                print(f"[DEBUG] Trying to locate RazorPay iframe (Attempt {attempt + 1}/3)")
                razor_pay_iframe = self.get_element(
                    "razor_pay_frame_xpath",
                    self.razor_pay_frame_xpath,
                    condition="presence"
                )
                self.switch_to_frame(razor_pay_iframe)
                print("[DEBUG] Successfully switched to RazorPay iframe")
                return

            except Exception as e:
                print(f"[WARN] Retry {attempt + 1}/3 failed -> {e}")
        raise Exception("Failed to switch to RazorPay iframe after 3 attempts")

    def click_on_show_qr(self):
        self.wait_for_element("show_qr_xpath", self.show_qr_xpath, condition="clickable")
        self.click_on_element("show_qr_xpath", self.show_qr_xpath)

    def click_on_continue(self):
        self.wait_for_element("continue_and_pay_xpath", self.continue_and_pay_xpath, condition="clickable")
        self.click_on_element("continue_and_pay_xpath", self.continue_and_pay_xpath)

    def verify_congratulation_text(self):
        self.switch_to_default_content()
        self.wait_for_stability()
        self.wait_for_element("congratulations_xpath", self.congratulations_xpath, condition="displayed")
        return self.get_message("congratulations_xpath", self.congratulations_xpath)

    def select_payment(self):
        self.switch_to_payment_window()
        self.click_on_show_qr()
        self.click_on_continue()
