import time
from pages.ParentPage import ParentPage


class InsurancePage(ParentPage):

    def __init__(self, driver):
        super().__init__(driver)

    insurance_for_everything_xpath = "//p[@class='font-size-28 mt-mob-3 text-white font-size-mob-20 font-weight-600']"
    accidental_xpath = "//p[normalize-space(text())='Accidental']"
    cancer_protect_xpath = "//p[@class='font-weight-600 font-size-16 text-black mb-0'][normalize-space()='Cancer Protect']"
    insurance_made_simple_xpath = "//p[normalize-space(text())='Insurance Made Simple']"
    insure_now_xpath = "//span[normalize-space(text())='Insure Now']"

    def verify_insurance_page(self):
        time.sleep(3)
        self.wait_for_element("insurance_for_everything_xpath", self.insurance_for_everything_xpath,
                              condition="displayed")
        self.get_message("insurance_for_everything_xpath", self.insurance_for_everything_xpath)

    def click_on_accidental(self):
        self.click_on_element("accidental_xpath", self.accidental_xpath, condition="clickable")

    def verify_insurance_made_simple_text(self):
        self.wait_for_element("insurance_made_simple_xpath", self.insurance_made_simple_xpath, condition="visible")
        self.get_message("insurance_made_simple_xpath", self.insurance_made_simple_xpath)

    def click_on_insure_now(self):
        self.wait_for_stability()
        self.click_on_element("insure_now_xpath", self.insure_now_xpath, condition="clickable", scroll=True)

    def click_on_cancer_protect(self):
        self.click_on_element("cancer_protect_xpath", self.cancer_protect_xpath, condition="clickable")

    def begin_product(self, product):
        product = product.lower()
        self.verify_insurance_page()
        if product == "accidental":
            self.click_on_accidental()
        elif product == "cancer":
            self.click_on_cancer_protect()
        else:
            raise Exception(f"Unsupported product type: {product}")
        self.verify_insurance_made_simple_text()
        self.click_on_insure_now()
