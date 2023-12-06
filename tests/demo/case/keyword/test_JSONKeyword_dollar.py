from loguru import logger

from tep.libraries.JSON import JSON


def test(JSONKeyword, VarKeyword):
    VarKeyword({
        'id': 9,
        'page': 9,
        'pin': "cekaigang",
        'a': 9,
        'ext': [1, 9, 1],
        'name': 'tep'
    })
    body = JSONKeyword(r"""
{
    "id":${id},
    "param":"[{\"page\": ${page}, \"pinList\":[\"${pin}\"]}]",
    "ext1":{
        "a":${a},
        "b":1
    },
    "ext2": ${ext},
    "ext3":{
        "name":"${name}"
    }
}
""")
    logger.info('\n' + JSON.beautify_json(JSON.to_json_str(body)))
