import time
from typing import Union
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ParentPage:
    def __init__(self,driver):
        self.driver =  driver

    def get_element(self, locator_name, locator_value, condition=None, timeout=20):

        locator_map = {
            "_id": By.ID,
            "_name": By.NAME,
            "_class": By.CLASS_NAME,
            "_tag": By.TAG_NAME,
            "_link_text": By.LINK_TEXT,
            "_partial_link_text": By.PARTIAL_LINK_TEXT,
            "_xpath": By.XPATH,
            "_css": By.CSS_SELECTOR
        }

        # determine locator strategy
        by = None
        for suffix, by_strategy in locator_map.items():
            if locator_name.lower().endswith(suffix):
                by = by_strategy
                break
        if not by:
            raise ValueError(f"Locator suffix not recognized in '{locator_name}'")

        wait = WebDriverWait(self.driver, timeout)

        # FRAME HANDLING
        if condition == "frame":
            return wait.until(EC.frame_to_be_available_and_switch_to_it((by, locator_value)))
            # No condition → simple find
        if condition is None:
            return self.driver.find_element(by, locator_value)

        # Other existing conditions
        try:
            if condition == "clickable":
                return wait.until(EC.element_to_be_clickable((by, locator_value)))
            elif condition == "visible":
                return wait.until(EC.visibility_of_element_located((by, locator_value)))
            elif condition == "presence":
                return wait.until(EC.presence_of_element_located((by,locator_value)))
            elif condition == "displayed":
                def is_displayed(driver):
                    try:
                        elem = driver.find_element(by, locator_value)
                        return elem if elem.is_displayed() else False
                    except (NoSuchElementException, StaleElementReferenceException):
                        return False

                return wait.until(is_displayed)
            else:
                raise ValueError("Invalid condition")
        except TimeoutException:
            print(f"Timeout: Element '{locator_name}' [{locator_value}] not {condition} after {timeout}s")
            raise

    def get_elements(self, locator_name, locator_value):
        locator_map = {
            "_id": By.ID,
            "_name": By.NAME,
            "_class": By.CLASS_NAME,
            "_tag": By.TAG_NAME,
            "_link_text": By.LINK_TEXT,
            "_partial_link_text": By.PARTIAL_LINK_TEXT,
            "_xpath": By.XPATH,
            "_css": By.CSS_SELECTOR
        }

        # Determine locator strategy
        by = None
        for suffix, by_strategy in locator_map.items():
            if locator_name.lower().endswith(suffix):
                by = by_strategy
                break

        if not by:
            raise ValueError(f"Locator suffix not recognized in '{locator_name}'")

        try:
            return self.driver.find_elements(by, locator_value)
        except Exception as e:
            print(f"Error finding elements: {locator_name} ({locator_value}) → {e}")
            return []


    def wait_for_element(self,locator_name,locator_value,condition=None,timeout=30):
        return self.get_element(locator_name,locator_value,condition=condition,timeout=timeout)

    def type_into_element(self,locator_name,locator_value,text):
        element = self.get_element(locator_name,locator_value)
        element.clear()
        element.send_keys(text)

    def click_on_element(self, locator_name, locator_value, condition = None, scroll=False, timeout=10):
        try:
            element = self.get_element(locator_name, locator_value, condition=condition, timeout=timeout)
            if scroll:
                self.scroll_into_view(element)
            try:
                element.click()
            except ElementClickInterceptedException:
                print(f"Click intercepted for '{locator_name}' - using JS click fallback.")
                self.driver.execute_script("arguments[0].click();", element)
            return element
        except TimeoutException:
            print(f"Timeout: Element '{locator_name}' ({locator_value}) not clickable after {timeout} seconds")
            raise
        except NoSuchElementException:
            print(f"Element not found: {locator_name} ({locator_value})")
            raise

    def get_message(self,locator_name,locator_value)-> str :
        element = self.get_element(locator_name,locator_value).text
        return element

    def display_status_of_element(self,locator_name,locator_value,timeout=10)-> bool :
        element = self.get_element(locator_name,locator_value,condition="displayed",timeout=timeout).is_displayed()
        return element

    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", element
        )
        return element

    def switch_to_frame(self,frame:Union[int,str,WebElement],timeout=5):
        wait = WebDriverWait(self.driver,timeout)
        if isinstance(frame,int):
            wait.until(EC.frame_to_be_available_and_switch_to_it(frame))
            print(f"[DEBUG] Switched_to_frame by index: {frame}")
            return
        elif isinstance(frame,str):
            try:
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID,frame)))
                print(f"[DEBUG] Switch_to_frame by ID: {frame}")
                return
            except TimeoutException:
                pass
            try:
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, frame)))
                print(f"[DEBUG] Switched_to_frame by Name:{frame}")
            except TimeoutException:
                raise TimeoutException(f"Frame not found by ID or NAME: {frame}")
            return
        elif isinstance(frame,WebElement):
            wait.until(EC.frame_to_be_available_and_switch_to_it(frame))
            print(f"[DEBUG] Switched_to_frame by WebElement")
            return
        else:
            raise ValueError("Frame must be int,str,or WebElement")

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def switch_to_parent_frame(self):
        self.driver.switch_to.parent_frame()

    def select_dropdown_by_text(self,option_xpath):
        self.wait_for_element("option_xpath",option_xpath,condition="visible",timeout=10)
        self.click_on_element("_xpath",option_xpath,condition="clickable")

    def wait_for_stability(self):
        time.sleep(1)