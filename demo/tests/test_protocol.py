import logging

from tep import request, v


class Data:
    v({
        'domain': 'https://postman-echo.com',
    })
    headers = {'User-Agent': 'tep'}
    body = {'foo1': 'foo1', 'foo2': 'foo2'}


def test():
    logging.info('run request with HTTP/1.1 and HTTP/2')

    logging.info('HTTP/1.1 get')
    response = request('get', url=v('${domain}/get'), headers=Data.headers, params=Data.body)
    assert response.status_code == 200
    assert len(Data.body['foo1']) == 4

    logging.info('HTTP/1.1 post')
    response = request('post', url=v('${domain}/post'), headers=Data.headers, json=Data.body)
    assert response.status_code == 200
    assert len(Data.body['foo1']) == 4

    logging.info('HTTP/2 get')
    response = request('get', url=v('${domain}/get'), headers=Data.headers, params=Data.body, http2=True)
    assert response.status_code == 200
    assert len(Data.body['foo1']) == 4

    logging.info('HTTP/2 post')
    response = request('post', url=v('${domain}/post'), headers=Data.headers, json=Data.body, http2=True)
    assert response.status_code == 200
    assert len(Data.body['foo1']) == 4
