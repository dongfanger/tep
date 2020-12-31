def test_a(faker_ch, env_vars):
    name = faker_ch.name()
    env_vars.put("name", name)
