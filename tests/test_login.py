from selenium.webdriver.common.by import By
import time

def login_flow(driver, base_url, email, password):
    driver.get(f"{base_url}/login")
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(0.5)

def test_login_happy_path(driver, base_url):
    login_flow(driver, base_url, "admin@example.com", "password123")
    assert "/dashboard" in driver.current_url
    assert "Bienvenido" in driver.page_source

def test_login_invalid(driver, base_url):
    login_flow(driver, base_url, "bad@x.com", "nope")
    assert "Credenciales incorrectas" in driver.page_source
