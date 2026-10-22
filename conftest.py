import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()

    yield browser

    browser.quit()
