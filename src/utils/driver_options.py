import platform

from selenium import webdriver

from src.utils.logger import Logger, LogLevel
from src.utils.error_handler import ErrorHandler, ErrorType

log = Logger(log_lvl=LogLevel.INFO).get_instance()


def _shared_driver_options(options):
    # ... (options setup)
    # options.add_argument("--headless")  # use headless with --no-sandbox
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    if platform.system() == "Linux":
        options.add_argument("--no-sandbox")
    log.info(f'Driver options {options.arguments}')
    return options


def _init_driver_options(dr_type=None):
    driver_option_mapping = {
        'local': webdriver.ChromeOptions(),
        'firefox': webdriver.FirefoxOptions()
    }

    options = driver_option_mapping.get(dr_type)

    if options is None:
        raise ErrorHandler.raise_error(ErrorType.UNSUPPORTED_DRIVER_TYPE, dr_type)

    _shared_driver_options(options)
    return options
