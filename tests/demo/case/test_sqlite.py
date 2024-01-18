from tep.libraries.Sqlite import Sqlite


def test():
    data = ("case_id", 1, "POST", "https://postman-echo.com/post", "123")
    Sqlite.create_table_replay()
    Sqlite.insert_into_replay_expect(data)
    Sqlite.update_replay_actual(("456", "case_id", 1, "POST", "https://postman-echo.com/post"))


def test_existed():
    data = ("f0350912ded65051be5f08a8b6b684ac", 2, "POST", "https://postman-echo.com/post", "123")
    print(Sqlite.is_replay_existed(data))


def test_get():
    results = Sqlite.get_expect_actual("f0350912ded65051be5f08a8b6b684ac")
    for row in results:
        expect, actual = row
        print(expect)
        print(actual)