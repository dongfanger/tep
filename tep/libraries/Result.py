from typing import Any, List, Union

from httpx import Response

from tep.libraries.TepResponse import TepResponse


class Result:
    # Http request, response
    response: List[Union[TepResponse, Response]] = None
    # Any data
    data: Any = None
    # Connect database, connection
    conn = None
    # Connect database, cursor
    cursor = None
