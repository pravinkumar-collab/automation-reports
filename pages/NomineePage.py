from pages.ParentPage import ParentPage


class NomineePage(ParentPage):

    def __init__(self, driver):
        super().__init__(driver)

    nominee_details_text_xpath = "//h1[contains(normalize-space(),'Nominee')]"
    fullName_xpath = "//input[@formcontrolname='name']"
    nomineAge_xpath = "//input[@formcontrolname='age']"
    relationship_xpath = "//mat-select[@formcontrolname='relationship']"
    nomineeMobile_xpath = "//input[@formcontrolname='mobile']"
    continue_xpath = "//span[normalize-space(text())='Continue']"

    nominee_name_warning_xpath = "//mat-error[normalize-space(.)='Full Name is required']"
    nominee_age_warning_xpath = "//mat-error[normalize-space(.)='Valid Nominee age must be between 18 to 110!']"
    nominee_relationship_warning_xpath = "//mat-error[contains(text(),'Please select your Relationship')]"
    nominee_mobile_warning_xpath = "//mat-error[contains(text(), 'Phone number is required')]"

    def verify_nominee_detail_text(self):
        self.wait_for_element("nominee_details_text_xpath", self.nominee_details_text_xpath, condition="displayed",
                              timeout=10)
        text = self.get_message("nominee_details_text_xpath", self.nominee_details_text_xpath)
        return text

    def enter_fullname(self, fullname_text):
        self.wait_for_stability()
        self.wait_for_element("fullName_xpath", self.fullName_xpath, condition="clickable", timeout=10)
        self.type_into_element("fullName_xpath", self.fullName_xpath, fullname_text)

    def enter_nominee_age(self, nominee_age_text):
        self.wait_for_stability()
        self.wait_for_element("nomineAge_xpath", self.nomineAge_xpath, condition="clickable", timeout=10)
        self.type_into_element("nomineAge_xpath", self.nomineAge_xpath, nominee_age_text)

    def select_relationship_type(self, relationship_type_text):
        self.click_on_element("relationship_xpath", self.relationship_xpath, condition="clickable", scroll=True)
        option_xpath = f"//mat-option//span[normalize-space()='{relationship_type_text}']"
        self.select_dropdown_by_text(option_xpath)

    def enter_nominee_mobile(self, nominee_mobile):
        self.wait_for_stability()
        self.type_into_element("nomineeMobile_xpath", self.nomineeMobile_xpath, nominee_mobile)

    def click_on_continue_button(self):
        self.click_on_element("continue_xpath", self.continue_xpath, condition="clickable", scroll=True)

    def complete_nominee_details(self, fullname_text, nominee_age_text, relationship_type_text, nominee_mobile):
        assert "Nominee" in self.verify_nominee_detail_text()
        self.enter_fullname(fullname_text)
        self.wait_for_stability()
        self.enter_nominee_age(nominee_age_text)
        self.select_relationship_type(relationship_type_text)
        self.enter_nominee_mobile(nominee_mobile)
        self.click_on_continue_button()

    def mandatory_nominee_details_warning(self):
        self.wait_for_element("fullName_xpath", self.fullName_xpath, condition="clickable", timeout=10)
        self.click_on_element("fullName_xpath", self.fullName_xpath)
        self.wait_for_stability()
        self.click_on_element("_tag", "body")
        nominee_name_msg = self.get_message("nominee_name_warning_xpath", self.nominee_name_warning_xpath)

        self.click_on_element("nomineAge_xpath", self.nomineAge_xpath)
        self.wait_for_stability()
        self.click_on_element("_tag", "body")
        nominee_age_msg = self.get_message("nominee_age_warning_xpath", self.nominee_age_warning_xpath)

        relationship_field = self.wait_for_element("relationship_xpath", self.relationship_xpath, condition="presence")
        self.driver.execute_script("arguments[0].focus();", relationship_field)
        self.wait_for_stability()
        self.driver.execute_script("arguments[0].blur();", relationship_field)
        self.wait_for_stability()
        nominee_relation_msg = self.get_message("nominee_relationship_warning_xpath",
                                                self.nominee_relationship_warning_xpath)

        self.click_on_element("nomineeMobile_xpath", self.nomineeMobile_xpath)
        self.wait_for_stability()
        self.click_on_element("_tag", "body")
        nominee_mobile_msg = self.get_message("nominee_mobile_warning_xpath", self.nominee_mobile_warning_xpath)

        return nominee_name_msg, nominee_age_msg, nominee_relation_msg, nominee_mobile_msg
