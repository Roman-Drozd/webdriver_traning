import time
from model.customer import Customer


def current_time_millis():
    return int(round(time.time() * 1000))


valid_customers = [Customer(firstname="Adam", lastname="Smith", phone="+0123456789",
                            address="Hidden Place", postcode="123456", city="New City",
                            country="US", zone="KS",
                            email="adam%s@smith.me" % current_time_millis(),
                            password="qwerty"),
                   # ...
                   ]
valid_product_count = [1, 3, 5]
