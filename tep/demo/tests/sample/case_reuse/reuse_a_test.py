from tests.sample.case_reuse.a_test import test_a


def test(faker_ch, env_vars):
    test_a(faker_ch, env_vars)
    print(env_vars.get("name"))
