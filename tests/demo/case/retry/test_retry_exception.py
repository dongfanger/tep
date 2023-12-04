from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(TypeError),
    before=lambda _: logger.info("Retrying..."),
    after=lambda _: logger.info("Retry completed.")
)
def test_exception(HTTPRequestKeyword):
    HTTPRequestKeyword("get", url="http://127.0.0.1:5000/retry/200")
    raise TypeError
