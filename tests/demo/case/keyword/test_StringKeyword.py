def test(VarKeyword, StringKeyword):
    VarKeyword({'domain': 'http://127.0.0.1:5000'})
    url = StringKeyword('${domain}/login')
    print(url)
