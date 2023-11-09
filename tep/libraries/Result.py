from typing import Any

from tep.libraries.TepResponse import TepResponse


class Result:
    # Http request, response
    response: TepResponse = None
    # Any data
    data: Any = None
    # Connect database, connection
    conn = None
    # Connect database, cursor
    cursor = None
