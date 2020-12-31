def test(env_vars):
    print(env_vars.domain)


def test_dynamic(env_vars):
    env_vars.put("hello", "2021")
    print(env_vars.get("hello"))


def test_your_name(env_vars_your_name):
    print(env_vars_your_name.your_var)
