from selenium.webdriver.common.by import By
import time

def test_update_property_negative_price(driver, base_url):
    # login
    driver.get(f"{base_url}/login")
    driver.find_element(By.NAME, "email").send_keys("admin@example.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(0.5)
    # create temp property to edit
    driver.get(f"{base_url}/properties/new")
    driver.find_element(By.NAME, "titulo").send_keys("Temp to edit")
    driver.find_element(By.NAME, "direccion").send_keys("Dir")
    driver.find_element(By.NAME, "precio").send_keys("100")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(0.5)
    # find edit link for the property and click (simple approach: go to dashboard and click first Edit)
    driver.get(f"{base_url}/dashboard")
    edit_links = driver.find_elements(By.LINK_TEXT, "Editar")
    assert len(edit_links) > 0
    edit_links[0].click()
    time.sleep(0.5)
    price_input = driver.find_element(By.NAME, "precio")
    price_input.clear()
    price_input.send_keys("-50")
    driver.find_element(By.TAG_NAME, "button").click()
    assert "Precio no puede ser negativo" in driver.page_source

def test_delete_property_cancel(driver, base_url):
    # Ensure login
    driver.get(f"{base_url}/login")
    driver.find_element(By.NAME, "email").send_keys("admin@example.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(0.5)
    # create a property to delete, then attempt delete but cancel via JS confirm override
    driver.get(f"{base_url}/properties/new")
    driver.find_element(By.NAME, "titulo").send_keys("ToDelete")
    driver.find_element(By.NAME, "direccion").send_keys("Addr")
    driver.find_element(By.NAME, "precio").send_keys("10")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(0.5)
    driver.get(f"{base_url}/dashboard")
    # override confirm to simulate cancel
    driver.execute_script("window.confirm = function(){ return false; };")
    delete_buttons = driver.find_elements(By.XPATH, "//button[text()='Eliminar']")
    if delete_buttons:
        delete_buttons[0].click()
    time.sleep(0.5)
    assert "ToDelete" in driver.page_source
