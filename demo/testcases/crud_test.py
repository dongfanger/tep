import jmespath
from loguru import logger
from tep.client import request

from testcases.conftest import fake, json_token_headers, env


def test(admin_login_token):
    admin_json_token_headers = json_token_headers(admin_login_token)

    logger.info('create')
    test_name = fake.name()
    body = {"name": test_name}
    response = request('post', url=env.test_url + '/api/create', headers=admin_json_token_headers, json=body)
    assert response.status_code < 400

    logger.info('retrieve')
    body = {"keyword": test_name}
    response = request('get', url=env.test_url + '/api/retrieve', headers=admin_json_token_headers, params=body)
    assert response.status_code < 400
    test_id = jmespath.search('id', response.json())

    logger.info('update')
    body = {"name": test_name + '-update'}
    response = request('put', url=env.test_url + f'/api/update/{test_id}', headers=admin_json_token_headers, json=body)
    assert response.status_code < 400

    logger.info('delete')
    response = request('delete', url=env.test_url + f'/api/roles/{test_id}', headers=admin_json_token_headers)
    assert response.status_code < 400
