一、GET
1.1 GET

```
request('get', url='')
```

1.2 GET、Header

```
request('get', url='', headers={})
```

1.3 GET、Header、查询参数
1.3.1 直接拼在url后面

```
request('get', url='' + '?a=1&b=2', headers={})
```

1.3.2 JSON转查询参数

```
from urllib.parse import urlencode

query = {}
request('get', url='' + '?' + urlencode(query), headers={})
```

1.4 GET、Header、表单

```
request('get', url='', headers={}, params={})
```

二、POST
2.1 POST

```
request('post', url='')
```

2.2 POST、Header

```
request('post', url='', headers={})
```

2.3 POST、Header、JSON

```
request('post', url='', headers={}, json={})
```

2.4 POST、Header、表单

```
request('post', url='', headers={}, data={})
```

三、PUT
3.1 PUT

```
request('put', url='')
```

3.2 PUT、Header

```
request('put', url='', headers={})
```

3.3 PUT、Header、JSON

```
request('put', url='', headers={}, json={})
```

3.4 PUT、Header、表单

```
request('put', url='', headers={}, data={})
```

四、DELETE
4.1 DELETE

```
request('delete', url='')
```

4.2 DELETE、Header

```
request('delete', url='', headers={})
```

五、上传文件
5.1 上传图片

```
files = {
    'file': ('filename', open('filepath', 'rb'), 'image/jpeg')
}
request('post', url='', headers={}, files=files)
```

注意requests会自动添加`{"Content-Type":"multipart/form-data"}`，使用headers不能再重复添加

5.2上传zip

```
files = {
    'file': ('filename', open('filepath', 'rb'), 'application/x-zip-compressed')
}
request('post', url='', headers={}, files=files)
```

六、Content Type

application/json
application/x-www-form-urlencoded