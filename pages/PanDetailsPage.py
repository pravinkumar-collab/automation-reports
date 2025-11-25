import time
from datetime import datetime
from pages.ParentPage import ParentPage


class PanDetailsPage(ParentPage):

    def __init__(self, driver):
        super().__init__(driver)

    # current_month_id = "mat-calendar-period-label-7"
    date_picker_xpath = "//button[@aria-label='Open calendar']//span[@class='mat-mdc-button-touch-target']"
    calendar_id = "mat-datepicker-0"
    year_dropdown_xpath = "//button[@aria-label='Choose month and year']//span[@class='mdc-button__label']"
    pan_number_xpath = "//input[@formcontrolname='pan_no']"
    gender_xpath = "//mat-label[normalize-space()='Select Your Gender']"
    male_option_xpath = "//span[text()='Male']"
    continue_xpath = "//span[normalize-space(text())='Continue']"

    dob_warning_xpath = "//mat-error[normalize-space(.)='Please input your birth date!']"
    pan_warning_xpath = "//mat-error[normalize-space(.)='PAN Number is required']"

    def select_date(self, date_string: str):

        # ---------- PREPARE DATE ----------
        date_string = date_string.replace("-", "/").replace(".", "/")
        target = datetime.strptime(date_string, "%d/%m/%Y")

        # ---------- LOCATORS ----------
        HEADER = ("_css", "button.mat-calendar-period-button span[aria-hidden='true']")
        HEADER_BTN = ("_css", "button.mat-calendar-period-button")

        PREV_24 = ("_xpath", "//button[@aria-label='Previous 24 years']")
        NEXT_24 = ("_xpath", "//button[@aria-label='Next 24 years']")

        NEXT_MONTH = ("_xpath", "//button[@aria-label='Next month']")
        PREV_MONTH = ("_xpath", "//button[@aria-label='Previous month']")

        target_month = target.strftime("%b").upper().replace("SEPT", "SEP")
        MONTH_CELL = ("_xpath", f"//span[normalize-space()='{target_month}']")
        YEAR_CELL = ("_xpath", f"//span[normalize-space()='{target.year}']")

        DAY_CELL = (
            "_xpath",
            f"//span[contains(@class,'mat-calendar-body-cell-content') "
            f"and normalize-space(text())='{target.day}']"
        )

        MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
                  "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

        # ---------- GET HEADER ----------
        def read_header():
            try:
                raw = self.get_element(*HEADER, condition="visible").text.strip()

                # CASE 1: Only year shown → "2025"
                if raw.isdigit():
                    return int(raw), None

                parts = raw.replace("\n", " ").split()

                # Now find year
                year = None
                for p in parts:
                    if p.isdigit() and len(p) == 4:
                        year = int(p)
                        break

                # Find the month text (anything not digit)
                month = None
                for p in parts:
                    if p.isalpha() and len(p) >= 3:
                        # Normalize month to uppercase short form
                        m = p[:3].upper()
                        if m == "SEPT":
                            m = "SEP"
                        month = m
                        break

                return year, month

            except Exception:
                return None, None

        # ---------- STEP 1: OPEN YEAR VIEW ----------
        displayed_year, displayed_month = read_header()

        if displayed_year == target.year and displayed_month == target_month:
            self.get_element(*DAY_CELL, condition="clickable").click()
            time.sleep(0.2)
            return

        if displayed_year == target.year and displayed_month is not None:
            while displayed_month != target_month:
                if MONTHS.index(displayed_month) < MONTHS.index(target_month):
                    self.get_element(*NEXT_MONTH, condition="clickable").click()
                else:
                    self.get_element(*PREV_MONTH, condition="clickable").click()
                time.sleep(0.1)
                displayed_year, displayed_month = read_header()
            self.get_element(*DAY_CELL, condition="clickable").click()
            return

        if displayed_year != target.year:
            self.get_element(*HEADER_BTN, condition="clickable").click()
            time.sleep(0.2)

            while True:
                all_labels = self.get_elements("_xpath", "//span[normalize-space()]")
                years = [int(i.text) for i in all_labels if i.text.isdigit()]

                if target.year in years:
                    # Select the year
                    self.get_element(*YEAR_CELL, condition="clickable").click()
                    time.sleep(0.1)

                    # Wait for month grid to appear
                    for _ in range(40):
                        yr, mn = read_header()
                        if mn is not None:
                            break
                        time.sleep(0.05)

                    # ❗ Critical: DO NOT RECLICK HEADER
                    # The month grid will auto-close otherwise
                    break

                if target.year < min(years):
                    self.get_element(*PREV_24, condition="clickable").click()
                else:
                    self.get_element(*NEXT_24, condition="clickable").click()

                time.sleep(0.1)

        # ---------- STEP 2: CLICK MONTH IMMEDIATELY ----------
        self.get_element(*MONTH_CELL, condition="clickable").click()
        time.sleep(0.1)

        # ---------- STEP 3: SELECT THE DAY ----------
        self.get_element(*DAY_CELL, condition="clickable").click()
        time.sleep(0.1)

        try:
            self.driver.execute_script("document.activeElement.blur();")
        except:
            pass

    def click_on_date_picker(self):
        self.click_on_element("date_picker_xpath", self.date_picker_xpath, condition="clickable")

    def wait_for_calendar(self):
        self.wait_for_element("calendar_id", self.calendar_id, condition="presence")

    def select_dob(self, date_string: str):
        self.click_on_date_picker()
        self.wait_for_stability()
        self.wait_for_calendar()
        self.select_date(date_string)

    def enter_pan_number(self, pan_text):
        self.type_into_element("pan_number_xpath", self.pan_number_xpath, pan_text)

    def select_gender(self, gender_text):
        self.click_on_element("gender_xpath", self.gender_xpath, condition="clickable")
        option_xpath = f"//*[normalize-space()='{gender_text}']"
        self.select_dropdown_by_text(option_xpath)

    def click_on_continue_button(self):
        self.click_on_element("continue_xpath", self.continue_xpath, condition="clickable", scroll=True)

    def close_calendar_if_open(self):
        try:
            calendar = self.get_element("calendar_id", self.calendar_id, condition="visible")
            if calendar:
                self.driver.execute_script("document.body.click()")
        except:
            pass

    def complete_pan_details(self, pan_text, gender_text):
        self.enter_pan_number(pan_text)
        self.close_calendar_if_open()
        self.select_gender(gender_text)
        self.click_on_continue_button()

    def mandatory_pan_details_warning(self):
        self.click_on_element("date_picker_xpath", self.date_picker_xpath, condition="clickable")
        self.wait_for_stability()
        self.click_on_element("_tag", "body")
        dob_msg = self.get_message("dob_warning_xpath", self.dob_warning_xpath)

        self.click_on_element("pan_number_xpath", self.pan_number_xpath)
        self.wait_for_stability()
        self.click_on_element("_tag", "body")
        pan_msg = self.get_message("pan_warning_xpath", self.pan_warning_xpath)

        return dob_msg, pan_msg
