import requests
from random import randint
from faker import Faker
from faker.providers import credit_card
import threading


def id_generator():
    check_list = []
    nums = []
    one = True

    # without the first number
    for i in range(8):
        num = randint(0, 9)
        nums.append(num)
        
        if one:
            check_list.append(num)
        else:
            if 2*num < 10:
                check_list.append(2 * num)
            else:
                check_list.append(int(str(2*num)[0]) + int(str(2*num)[1]))

        one = not one

    first = sum(check_list) % 10
    rest = "".join([str(num) for num in nums])
    return f"{first}{rest}"


def do_request():
    url = "hidden"

    fake = Faker()
    fake.add_provider(credit_card)
    expire = fake.credit_card_expire().split('/')

    data = {
        "nocphone2": id_generator(),  # id
        "name": fake.name(),  # name
        "ccnn1": fake.credit_card_number(),  # card number
        "cexppdm": expire[0],  # expired month
        "cexdyyyyss": expire[1],  # expired year
        "qsdq21sd5s4d4s1": fake.credit_card_security_code(),  # cvv
        "submit": "submit"  # static value
    }

    response = requests.post(url, data=data).text
    print("response text" + response)


threads = []

for i in range(50):
    t = threading.Thread(target=do_request)
    t.daemon = True
    threads.append(t)

for i in range(50):
    threads[i].start()

for i in range(50):
    threads[i].join()
