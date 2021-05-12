import pdb
from uuid import uuid4

from upwork import settings
from upwork.logging import get_logger

logger = get_logger(__name__)


def screenshot(driver, filepath=None):
    filepath = filepath or f'{uuid4()}.png'
    logger.critical(f'Saving screenshot for troubleshooting in {filepath}')
    driver.save_screenshot(filepath)


def handle_exception(exception, driver):
    logger.critical(f'{exception}')
    screenshot(driver)
    if settings.DEBUG:
        pdb.set_trace()
    else:
        driver.quit()
        raise exception


def driver_except(f):
    def wrapper(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except Exception as e:
            handle_exception(e, self.driver)

    return wrapper
