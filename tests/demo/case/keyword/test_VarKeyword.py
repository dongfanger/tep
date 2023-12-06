def test(VarKeyword):
    var = VarKeyword({'id': 9})
    print(var["id"])
    var["name"] = "pytest"
    print(VarKeyword())
