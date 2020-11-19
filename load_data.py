import getopt
from faker import Faker
import os
from random import seed
from random import randint
import stripe
import sys
import logging

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

fake = Faker()
stripe.api_key = os.environ['STRIPE_API_KEY']


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
    num_customers = 0
    num_invoices = 0
    num_charges = 0
    try:
        opts, _ = getopt.getopt(argv, 'hn:i:c:')
    except getopt.GetoptError:
        print('load_data.py -n <number-of-customers> -i <invoices-per-customer> -c <charges-per-customer>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('load_data.py -n <number-of-customers>')
            sys.exit()
        elif opt in ("-n") and arg.isnumeric():
            num_customers = int(arg)
        elif opt in ("-i") and arg.isnumeric():
            num_invoices = int(arg)
        elif opt in ("-c") and arg.isnumeric():
            num_charges = int(arg)
    if num_customers <= 0:
        print('ERROR: Number of customers should be a positive integer')
        sys.exit()
    if num_invoices <= 0:
        print('ERROR: Number of invoices should be a positive integer')
        sys.exit()
    if num_charges <= 0:
        print('ERROR: Number of charges should be a positive integer')
        sys.exit()
    seed(1)
    for _ in range(num_customers):
        try:
            customer_id = create_customer()
            for _ in range(num_invoices):
                create_invoice(customer_id)
            for _ in range(num_charges):
                create_charge(customer_id)
            logging.info('Created customer, charges and invoices. Customer id: %s', customer_id)
        except:
            logging.warning('ERROR: Could not create data. Skipping to next iteration!')


if __name__ == "__main__":
    main(sys.argv[1:])
