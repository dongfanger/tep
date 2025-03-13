import uvicorn
from fastapi import FastAPI, Request

'''
Please install fastapi:
pip install "fastapi[standard]"
'''


app = FastAPI()


@app.post('/login')
async def login(req: Request):
    body = await req.json()
    if body['username'] == 'dongfanger' and body['password'] == '123456':
        return {'Cookie': 'de2e3ffu29'}
    return ''


@app.get('/searchSku')
async def search_sku(req: Request):
    if req.headers.get('Cookie') == 'de2e3ffu29' and req.query_params.get('skuName') == 'book':
        return {'skuId': '222', 'price': '2.3'}
    return ''


@app.post('/addCart')
async def add_cart(req: Request):
    body = await req.json()
    if req.headers.get('Cookie') == 'de2e3ffu29' and body['skuId'] == '222':
        return {'skuId': '222', 'price': '2.3', 'skuNum': 3, 'totalPrice': '6.9'}
    return ''


@app.post('/order')
async def order(req: Request):
    body = await req.json()
    if req.headers.get('Cookie') == 'de2e3ffu29' and body['skuId'] == '222':
        return {'orderId': '333'}
    return ''


@app.post('/pay')
async def pay(req: Request):
    body = await req.json()
    if req.headers.get('Cookie') == 'de2e3ffu29' and body['orderId'] == '333':
        return {'success': 'true'}
    return ''


@app.get('/retry/code', status_code=500)
async def retry_code(req: Request):
    return {'success': 'false'}


if __name__ == '__main__':
    uvicorn.run('mock:app', host='127.0.0.1', port=5000)
