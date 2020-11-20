# calixa-test

You should create an environment variable called STRIPE_API_KEY with your stripe api key.

Before running any script, execute the following commands:
```
$ virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

How to load data:
```$ python load_data.py -n <num-customers> -i <num-invoices> -c <num-charges>```

How to run the REST app:
```$ python app.py```

Validate data made it to the app:
```$ curl --location --request GET 'http://localhost:5002/customer-status'```