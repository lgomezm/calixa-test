N = 10
customer_status_store = {}

def add_customer_status(status):
    """Stores a customer status. If there was already N status objects
    for the customer, it drops the oldest one and returns true.
    Otherwise, it just stores the status and returns false""" 
    customer = status.customer
    if customer not in customer_status_store:
        customer_status_store[customer] = []
    customer_status = customer_status_store[customer]
    dropped = False
    if len(customer_status) == N:
        customer_status.pop(0)
        dropped = True
    customer_status.append(status)
    return dropped

def get_all_customer_status():
    """Returns all the contents of the customer status store"""
    return customer_status_store
