from pages.ParentPage import ParentPage

class SuperappPage(ParentPage):

    def __int__(self,driver):
        super().__init__(driver)

    home_partial_link_text = "Home"
    insurance_partial_link_text = "Insurance"

    def home_is_displayed(self):
        assert self.display_status_of_element("home_partial_link_text",self.home_partial_link_text)

    def click_on_insurance_section(self):
        self.click_on_element("insurance_partial_link_text",self.insurance_partial_link_text)
