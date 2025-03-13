def test_assert_equal():
    assert 1 == 1


def test_assert_not_equal():
    assert 1 != 2


def test_assert_greater_than():
    assert 2 > 1


def test_assert_less_than():
    assert 1 < 2


def test_assert_greater_or_equals():
    assert 2 >= 1
    assert 1 >= 1


def test_assert_less_or_equals():
    assert 1 <= 2
    assert 2 <= 2


def test_assert_length_equal():
    assert len('abc') == len('123')


def test_assert_length_greater_than():
    assert len('hello') > len('123')


def test_assert_length_less_than():
    assert len('hi') < len('123')


def test_assert_length_greater_or_equals():
    assert len('hello') >= len('123')
    assert len('123') >= len('123')


def test_assert_length_less_or_equals():
    assert len('123') <= len('hello')
    assert len('123') <= len('123')


def test_assert_string_equals():
    assert 'dongfanger' == 'dongfanger'


def test_assert_startswith():
    assert 'dongfanger'.startswith('don')


def test_assert_endswith():
    assert 'dongfanger'.endswith('er')


def test_assert_regex_match():
    import re
    assert re.findall(r'don.*er', 'dongfanger')


def test_assert_contains():
    class Res:
        code = 200
        msg = 'success'

    assert 'success' in Res.msg
    assert 2 in [2, 3]
    assert 'x' in {'x': 'y'}.keys()


def test_assert_contained_by():
    class Res:
        code = 200
        msg = 'success'

    assert Res.code in [0, 200]


def test_assert_type_match():
    assert isinstance(1, int)
    assert isinstance(0.2, float)
    assert isinstance(True, bool)
    assert isinstance(3e+26j, complex)
    assert isinstance('hi', str)
    assert isinstance([1, 2], list)
    assert isinstance((1, 2), tuple)
    assert isinstance({'a', 'b', 'c'}, set)
    assert isinstance({'x': 1}, dict)
