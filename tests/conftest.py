import os
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from datetime import datetime

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
REPORT_DIR = os.path.join(os.getcwd(), "reports")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

@pytest.fixture(scope='session')
def base_url():
    return "http://localhost:5000"

@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # uncomment for headless runs
    service = ChromeService(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        driver = item.funcargs.get("driver", None)
        if driver is not None:
            fname = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}-{item.name}.png"
            path = os.path.join(SCREENSHOT_DIR, fname)
            try:
                driver.save_screenshot(path)
                # attach path to report if pytest-html available
                if hasattr(rep, 'extra'):
                    rep.extra.append(path)
                else:
                    rep.extra = [path]
            except Exception as e:
                print('No se pudo guardar screenshot:', e)
