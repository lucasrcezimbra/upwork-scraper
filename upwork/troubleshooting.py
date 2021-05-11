import logging
from uuid import uuid4

# TODO: improve log format
logger = logging.getLogger(__name__)


def screenshot(driver, filepath=None):
    filepath = filepath or f'{uuid4()}.png'
    logger.critical(f'Saving screenshot for troubleshooting in {filepath}')
    driver.save_screenshot(filepath)


def driver_except(f):
    def wrapper(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except Exception as e:
            logger.critical(f'{e}')
            screenshot(self.driver)
            raise e
        # finally:
        #     # TODO: keep open when debuging
        #     self.driver.quit()

    return wrapper
