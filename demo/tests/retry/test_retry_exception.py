import logging

from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from tep import request


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(TypeError),
    before=lambda _: logging.info('Retrying...'),
    after=lambda _: logging.info('Retry completed.')
)
def test_exception():
    request('get', url='http://127.0.0.1:5000/retry/200')
    raise TypeError
