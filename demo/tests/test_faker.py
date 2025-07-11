from faker import Faker
from tep import logger


def test():
    logger.info(Faker().name())
    logger.info(Faker(locale='zh_CN').name())
    logger.info(Faker(locale='en').name())
