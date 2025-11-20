import logging
import allure
import requests
from allure_commons.types import AttachmentType
from seleniumwire import webdriver   # <---- use this, not "from selenium"
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from utilities.config_reader import get_config

# ============================================================
# 🔇 CLEAN ALL NOISY LOGS (Keep Allure Clean)
# ============================================================
logging.getLogger("seleniumwire").setLevel(logging.CRITICAL)
logging.getLogger("selenium").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("PIL").setLevel(logging.CRITICAL)
logging.getLogger("matplotlib").setLevel(logging.CRITICAL)
# ============================================================


@pytest.fixture(scope="class",autouse=True)
def setup_and_teardown(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    options.add_experimental_option("useAutomationExtension",False)
    options.add_argument("--disable-infobars")
    options.add_argument('ignore-certificate-errors')
    options.add_argument("--disable-application-cache")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=options,seleniumwire_options={'verify_ssl': False})
    driver.maximize_window()
    app_url = get_config("basic details","url")
    driver.get(app_url)
    request.cls.driver = driver
    yield driver
    if driver:
        try:
            driver.quit()
        except:
            pass


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Capture screenshot ONLY when test body ("call") fails
    if report.when != "call" or not report.failed:
        return

    driver = None

    # --- 1) Try to get driver from your actual fixture ---
    if "setup_and_teardown" in item.funcargs:
        driver = item.funcargs["setup_and_teardown"]

    # --- 2) Try to get driver from class instance (safe check) ---
    instance = getattr(item, "instance", None)
    if not driver and instance and hasattr(instance, "driver"):
        driver = instance.driver

    # --- If driver still not found, do nothing ---
    if not driver:
        print("[WARN] Driver not found for screenshot capturing")
        return

    # --- ATTACH SCREENSHOT ---
    try:
        png = driver.get_screenshot_as_png()
        allure.attach(
            png,
            name=f"{item.name}_failed",
            attachment_type=AttachmentType.PNG
        )
        print("[INFO] Screenshot added to Allure")
    except Exception as e:
        print("[ERROR] Could not take screenshot:", e)


@pytest.fixture(scope="class",autouse=True)
def delete_user_before_test():
    delete_api = get_config("deleteApi url","url")
    mobile_number = get_config("deleteApi url","user number")
    api_token = get_config("deleteApi url","token")
    headers = {"Content-Type": "application/json",
               "Authorization":f"Token {api_token}"
               }
    payload = {
        "users":[mobile_number]
    }
    print("\n[INFO] Deleting User before test")
    print()
    try:
        response = requests.post(delete_api,json=payload,headers=headers)
        if response.status_code == 200:
            print(f"[INFO] User deleted successfully: {response.json()}")
        else:
            print(f"[WARN] User is not deleted: '({response.status_code}:{response.text})'")
    except Exception as e:
        print(f"[ERROR] User deletion failed due to: {e}")
    yield

