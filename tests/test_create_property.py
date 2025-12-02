from selenium.webdriver.common.by import By
import time

def test_create_property_happy_path(driver, base_url):
    # login first
    driver.get(f"{base_url}/login")
    driver.find_element(By.NAME, "email").send_keys("admin@example.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(0.5)
    driver.get(f"{base_url}/properties/new")
    driver.find_element(By.NAME, "titulo").send_keys("Apartamento Centro")
    driver.find_element(By.NAME, "direccion").send_keys("Calle 1 #2")
    driver.find_element(By.NAME, "precio").send_keys("85000")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(0.5)
    assert "Apartamento Centro" in driver.page_source

def test_create_property_missing_title(driver, base_url):
    driver.get(f"{base_url}/properties/new")
    driver.find_element(By.NAME, "titulo").clear()
    driver.find_element(By.NAME, "direccion").send_keys("Calle sin titulo")
    driver.find_element(By.NAME, "precio").send_keys("1000")
    driver.find_element(By.TAG_NAME, "button").click()
    assert "Titulo y precio son obligatorios" in driver.page_source
