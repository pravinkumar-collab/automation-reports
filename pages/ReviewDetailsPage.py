from pages.ParentPage import ParentPage


class ReviewDetailsPage(ParentPage):

    def __init__(self, driver):
        super().__init__(driver)

    total_payable_amount_xpath = "//p[normalize-space()='Total Payable Amount:']"
    proceed_xpath = "//button[contains(@class,'w-30p') and .//span[normalize-space()='Proceed']]"

    def verify_display_of_amount_field(self):
        self.wait_for_element("total_payable_amount_xpath", self.total_payable_amount_xpath, condition="displayed")
        self.get_message("total_payable_amount_xpath", self.total_payable_amount_xpath)

    def click_on_proceed_button(self):
        self.wait_for_element("proceed_xpath", self.proceed_xpath, condition="clickable")
        self.wait_for_stability()
        self.click_on_element("proceed_xpath", self.proceed_xpath, condition="clickable", scroll=True)
