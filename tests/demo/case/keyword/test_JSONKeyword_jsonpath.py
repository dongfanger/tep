import json

from loguru import logger


def test(JSONKeyword):
    body = r"""{"id":1,"param":"[{\"page\": 1, \"pinList\":[\"cekaigang\"]}]","ext1":{"a":1,"b":1},"ext2":[1,1,1],"ext3":{"name":"pytest"}}"""
    body = JSONKeyword(body, {"$.id": 9, "$.param[0].page": 9, "$.param[0].pinList[0]": "dongfanger", "$.ext1.a": 9, "$.ext2[0]": 9, "$.ext2[2]": 9, "$.ext3.name": "tep"})
    logger.info(json.dumps(body, ensure_ascii=False))
