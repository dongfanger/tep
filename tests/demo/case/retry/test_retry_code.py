from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    before=lambda _: logger.info("Retrying..."),
    after=lambda _: logger.info("Retry completed.")
)
def test(HTTPRequestKeyword):
    ro = HTTPRequestKeyword("get", url="http://127.0.0.1:5000/retry/code")
    ro.response.raise_for_status()  # Add this statement