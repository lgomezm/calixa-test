import json


class CustomerStatus:
    def __init__(self, customer, amount, status, object_type):
        self.customer = customer
        self.amount = amount
        self.status = status
        self.object_type = object_type
