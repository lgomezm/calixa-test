from dao import customer_status_dao
from flask import Flask, request
import os
import stripe

stripe.api_key = os.environ['STRIPE_API_KEY']
app = Flask(__name__)

N = 10
customer_events = {}

@app.route('/stripe', methods=['POST'])
def store_stripe_event():
    body = request.json
    event = None
    try:
        event = stripe.Event.construct_from(body, stripe.api_key)
    except ValueError:
        return {'error': 'Could not parse event'}
    record = None
    try:
        data = event.data.object
        record = {
            'customer': data.customer,
            'status': data.status,
            'type': data.object,
            'amount': data.amount
        }
    except AttributeError:
        return {'error': 'Could not get one of expected attributes: [customer, amount, status]'}
    if record['customer'] is None:
        return {'error': 'customer is null'}
    customer_status_dao.add_customer_status(record)
    return {}


@app.route('/customer-status', methods=['GET'])
def get_customer_status():
    return customer_status_dao.get_all_customer_status()

if __name__ == '__main__':
    app.run(port='5002')
