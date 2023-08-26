import os

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# Initialize the WebDriver options
def init_driver_options():
    opts = webdriver.ChromeOptions()
    # ... (options setup)
    # opts.add_argument("--headless")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    return opts


# Create a function to create the WebDriver instance
def create_driver():
    try:
        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            options=init_driver_options(),
        )
    except Exception as e:
        print(f"Failed to install ChromeDriver: {e}")
        driver = webdriver.Chrome(
            executable_path=get_driver_path(), options=init_driver_options()
        )
    driver.maximize_window()
    return driver


def get_driver_path(driver_name="chromedriver"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(script_dir, "resources")
    driver_path = os.path.join(resources_dir, driver_name)
    return driver_path


def quit_driver(driver):
    if driver is not None:
        driver.quit()


# Change scope to "function" to ensure separate drivers create for each test function to avoin issues
# in multithread, but this increases time execution and memory usage
@pytest.fixture(scope="session")
def make_driver(request) -> webdriver.Remote:
    driver = None

    def _make_driver() -> webdriver.Remote:
        nonlocal driver
        driver = create_driver()
        return driver

    yield _make_driver()
    quit_driver(driver)


# Command line options to specify the browser version
def pytest_addoption(parser):
    parser.addoption("--browser-version", action="store", default="116", help="Specify the browser version")


@pytest.fixture(scope="session")
def browser_version(request):
    return request.config.getoption("--browser-version", "116")