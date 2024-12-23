import logging

from tenacity import retry, stop_after_attempt, wait_fixed
from tep import request


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    before=lambda _: logging.info("Retrying..."),
    after=lambda _: logging.info("Retry completed.")
)
def test():
    response = request("get", url="http://127.0.0.1:5000/retry/code")
    response.raise_for_status()  # Add this statement
