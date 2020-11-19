from dao import customer_status_dao
import encoder
from model import model
from flask import Flask, request
import os
import stripe

stripe.api_key = os.environ['STRIPE_API_KEY']

app = Flask(__name__)
app.json_encoder = encoder.MyEncoder


@app.route('/stripe', methods=['POST'])
def store_stripe_event():
    body = request.json
    event = None
    try:
        event = stripe.Event.construct_from(body, stripe.api_key)
    except ValueError:
        return {'error': 'Could not parse event'}
    customer_status = None
    try:
        data = event.data.object
        customer_status = model.CustomerStatus(
            customer=data.customer,
            amount=data.amount,
            status=data.status,
            object_type=data.object
        )
    except AttributeError:
        return {'error': 'Could not get one of expected attributes: [customer, amount, status]'}
    if customer_status.customer is None:
        return {'error': 'customer is null'}
    customer_status_dao.add_customer_status(customer_status)
    return {}


@app.route('/customer-status', methods=['GET'])
def get_customer_status():
    return customer_status_dao.get_all_customer_status()

if __name__ == '__main__':
    app.run(port='5002')
