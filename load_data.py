import getopt
from faker import Faker
from random import seed
from random import randint
import stripe
import sys

fake = Faker()

stripe.api_key = "pk_test_51HobYRHLGNtIeaaJJvGLE311aGRFwFKj1GJubdrHcNCqq3hiyqpjiQzryvZd0LZtYm9Nd7pOj0R05zpuyeOmcE9C00TFkjHMov"

def create_customer():
    """Creates a customer in the stripe account"""
    resp = stripe.Customer.create(
        email=fake.email(),
        name=fake.name()
    )
    customer_id = resp.id
    stripe.Customer.create_source(
        customer_id,
        source='tok_visa',
    )
    return customer_id

def create_charge(customer_id):
    """Creates a customer with a random amount"""
    stripe.Charge.create(
        amount=randint(50, 10000),
        currency='usd',
        customer=customer_id
    )

def create_invoice(customer_id):
    """Creates an invoice with a random amount"""
    price = stripe.Price.create(
        unit_amount=randint(50, 10000),
        currency='usd',
        product_data={'name': 'product'}
    )
    stripe.InvoiceItem.create(
        customer=customer_id,
        price=price.id,
    )
    stripe.Invoice.create(
        customer=customer_id,
        auto_advance=True
    )


def main(argv):
    n = 0
    try:
        opts, _ = getopt.getopt(argv, 'hn:')
    except getopt.GetoptError:
        print('load_data.py -n <number-of-customers>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('load_data.py -n <number-of-customers>')
            sys.exit()
        elif opt in ("-n") and arg.isnumeric():
            n = int(arg)
    if n <= 0:
        print('Number of customers should be a positive integer')
    seed(1)
    for _ in range(0, n):
        try:
            customer_id = create_customer()
            create_invoice(customer_id)
            create_charge(customer_id)
            print('Created customer, charge and invoice. Customer id:', customer_id)
        except:
            print('Could not create data!')


if __name__ == "__main__":
    main(sys.argv[1:])
