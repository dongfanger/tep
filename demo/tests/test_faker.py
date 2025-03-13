from faker import Faker


def test():
    print(Faker().name())
    print(Faker(locale='zh_CN').name())
    print(Faker(locale='en').name())
