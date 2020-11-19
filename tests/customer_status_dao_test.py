import unittest
from dao import customer_status_dao
from model import model

class TestCustomerStatusDao(unittest.TestCase):

    def test_add_one_customer_status_succeeds(self):
        status = create_customer_status_with_amount('customer1', 5000)
        customer_status_dao.add_customer_status(status)
        all_status = customer_status_dao.get_all_customer_status()
        self.assertIn('customer1', all_status)

    def test_add_multiple_customer_status_succceds(self):
        status_to_add = [create_customer_status_with_amount('customer2', i) for i in range(1, 11)]
        for status in status_to_add:
            customer_status_dao.add_customer_status(status)
        all_status = customer_status_dao.get_all_customer_status()
        self.assertEqual(10, len(all_status['customer2']))

    def test_add_more_than_n_customer_status_succceds(self):
        n = customer_status_dao.N
        status_to_add = [create_customer_status_with_amount('customer3', i) for i in range(n)]
        for status in status_to_add:
            customer_status_dao.add_customer_status(status)
        # Validate all n status have made it and validate the oldest one is stored
        all_status = customer_status_dao.get_all_customer_status()
        self.assertEqual(n, len(all_status['customer3']))
        self.assertTrue([s for s in all_status['customer3'] if s.amount == 0])
        # Add one more status for the same customer and validate the oldest one is not stored anymore
        customer_status_dao.add_customer_status(create_customer_status_with_amount('customer3', n))
        all_status = customer_status_dao.get_all_customer_status()
        self.assertEqual(n, len(all_status['customer3']))
        self.assertTrue([s for s in all_status['customer3'] if s.amount == n])
        self.assertFalse([s for s in all_status['customer3'] if s.amount == 0])


def create_customer_status_with_amount(customer, amount):
    return model.CustomerStatus(
        customer=customer,
        amount=amount,
        status='succeeded',
        object_type='charge'
    )


if __name__ == '__main__':
    unittest.main()