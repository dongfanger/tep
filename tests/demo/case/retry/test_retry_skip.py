from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    before=lambda _: logger.info("Retrying..."),
    after=lambda _: logger.info("Retry completed.")
)
def test_req(HTTPRequestKeyword):
    response = HTTPRequestKeyword("get", url="http://127.0.0.1:5000/retry/code")
    response.raise_for_status()  # Add this statement


def test():
    try:
        test_req()
    except Exception as e:
        logger.warning('Max retries exceeded:', e)
