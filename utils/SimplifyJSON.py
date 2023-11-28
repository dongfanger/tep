import json


def simplify_json(json_str: str) -> str:
    data = json.loads(json_str)
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False)


if __name__ == '__main__':
    json_str = r"""
{
       "orderId": 1,
       "payAmount": "0.2"
}
"""
    print(simplify_json(json_str))
