
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


BASE_URL = "https://www.testmuai.com/selenium-playground/"


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    yield browser
    browser.quit()


def open_playground(driver):
    driver.get(BASE_URL)
    return WebDriverWait(driver, 15)


def test_simple_form_demo(driver):
    wait = open_playground(driver)

    # Open Simple Form Demo
    wait.until(EC.element_to_be_clickable(
        (By.LINK_TEXT, "Simple Form Demo")
    )).click()

    # Verify URL
    wait.until(EC.url_contains("simple-form-demo"))

    # Enter a message using a variable
    message = "Welcome to TestMu AI"
    message_box = wait.until(EC.visibility_of_element_located(
        (By.ID, "user-message")
    ))
    message_box.send_keys(message)

    # Click Get Checked Value
    wait.until(EC.element_to_be_clickable(
        (By.ID, "showInput")
    )).click()

    # Verify displayed message
    displayed_message = wait.until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert displayed_message.text == message


def test_drag_drop_slider(driver):
    wait = open_playground(driver)

    # Open Drag & Drop Sliders
    wait.until(EC.element_to_be_clickable(
        (By.LINK_TEXT, "Drag & Drop Sliders")
    )).click()

    # Locate the slider whose default value is 15
    slider = wait.until(EC.visibility_of_element_located((
        By.XPATH,
        "//input[@type='range' and @value='15']"
    )))

    # Move the slider to 95 using keyboard controls.
    # This avoids relying on pixel coordinates.
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", slider
    )
    slider.click()
    slider.send_keys("HOME")

    for _ in range(95):
        slider.send_keys("ARROWRIGHT")

    # Verify slider value
    value = slider.get_attribute("value")
    assert value == "95", f"Expected 95, got {value}"


def test_input_form_submit(driver):
    wait = open_playground(driver)

    # Open Input Form Submit
    wait.until(EC.element_to_be_clickable(
        (By.LINK_TEXT, "Input Form Submit")
    )).click()

    # Click Submit without filling the form
    submit_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']")
    ))
    submit_button.click()

    # Verify browser's required-field validation
    name_field = wait.until(EC.presence_of_element_located(
        (By.NAME, "name")
    ))
    assert name_field.get_attribute("required") is not None
    assert driver.execute_script(
        "return arguments[0].validity.valueMissing;", name_field
    )

    # Fill in the required fields
    name_field.send_keys("Test User")

    driver.find_element(By.NAME, "email").send_keys(
        "testuser@example.com"
    )
    driver.find_element(By.NAME, "password").send_keys("TestPass123!")

    driver.find_element(By.NAME, "company").send_keys("Test Company")
    driver.find_element(By.NAME, "website").send_keys(
        "https://example.com"
    )

    # Select country by visible text
    country_dropdown = Select(
        driver.find_element(By.NAME, "country")
    )
    country_dropdown.select_by_visible_text("United States")

    driver.find_element(By.NAME, "city").send_keys("New York")
    driver.find_element(By.NAME, "address_line1").send_keys(
        "123 Test Street"
    )
    driver.find_element(By.NAME, "address_line2").send_keys(
        "Suite 10"
    )
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "zip").send_keys("10001")

    # Submit the completed form
    submit_button.click()

    # Verify success message
    success_message = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//*[contains(normalize-space(.), "
            "'Thanks for contacting us, we will get back to you shortly.')]"
        ))
    )

    assert (
        "Thanks for contacting us, we will get back to you shortly."
        in success_message.text
    )
