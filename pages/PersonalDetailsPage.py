from pages.ParentPage import ParentPage
from pages.SuperappPage import SuperappPage


class PersonalDetailsPage(ParentPage):

    def __init__(self,driver):
        super().__init__(driver)

    firstName_xpath = "//input[@placeholder='First Name']"
    middleName_xpath = "//mat-label[normalize-space()='Middle Name (Optional)']"
    lastname_xpath = "//input[@placeholder='Last Name']"
    email_xpath = "//input[@placeholder='Email']"
    pincode_xpath = "//input[@placeholder='Pincode']"

    continue_button_xpath="//button[@type='submit']"
    firstName_warning_xpath = "//mat-error[normalize-space()='First Name is required']"
    lastName_warning_xpath = "//mat-error[normalize-space()='Last Name is required']"
    email_warning_xpath = "//mat-error[normalize-space()='Email is required']"
    pincode_warning_xpath = "//mat-error[normalize-space()='Pincode is required']"


    def enter_firstname(self,firstname_text):
        self.wait_for_element("firstName_xpath",self.firstName_xpath,condition="visible")
        self.type_into_element("firstName_xpath",self.firstName_xpath,firstname_text)

    def enter_middlename(self,middlename_text):
        self.type_into_element("middleName_xpath",self.middleName_xpath,middlename_text)

    def enter_lastname(self,lastname_text):
        self.type_into_element("lastname_xpath",self.lastname_xpath,lastname_text)

    def enter_email(self,email_text):
        self.type_into_element("email_xpath",self.email_xpath,email_text)

    def enter_pincode(self,pincode_number):
        self.type_into_element("pincode_xpath",self.pincode_xpath,pincode_number)

    def click_on_continue(self):
        self.click_on_element("continue_button_xpath",self.continue_button_xpath,condition="clickable")
        return SuperappPage

    def enter_personal_details(self,firstname_text,lastname_text,email_text,pincode_number,middlename_text=None,is_mandatory= False):
        self.enter_firstname(firstname_text)
        self.enter_lastname(lastname_text)
        self.enter_email(email_text)
        self.enter_pincode(pincode_number)
        if is_mandatory and middlename_text:
            self.enter_middlename(middlename_text)
        self.click_on_continue()


    def mandatory_register_yourself_warning(self):
        self.wait_for_element("firstName_xpath",self.firstName_xpath,condition="visible")
        self.click_on_element("firstName_xpath",self.firstName_xpath)
        self.wait_for_stability()
        self.click_on_element("_tag","body")
        firstname_msg = self.get_message("firstName_warning_xpath",self.firstName_warning_xpath)

        self.click_on_element("lastname_xpath",self.lastname_xpath)
        self.wait_for_stability()
        self.click_on_element("_tag","body")
        lastname_msg = self.get_message("lastName_warning_xpath",self.lastName_warning_xpath)

        self.click_on_element("email_xpath",self.email_xpath)
        self.wait_for_stability()
        self.click_on_element("_tag","body")
        email_msg = self.get_message("email_warning_xpath",self.email_warning_xpath)

        self.click_on_element("pincode_xpath",self.pincode_xpath)
        self.wait_for_stability()
        self.click_on_element("_tag","body")
        pincode_msg = self.get_message("pincode_warning_xpath",self.pincode_warning_xpath)

        return firstname_msg, lastname_msg, email_msg, pincode_msg