import unittest
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sshp.models.Purchase import Purchase


class TestPurchase(unittest.TestCase):
    engine = create_engine('sqlite:///../data/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    def test_add_purchase(self):
        purchase_date = date.today()
        garment_name = "testing"
        product_code = "100-100-10-0100"
        quantity = 10

        purchase = (purchase_date, garment_name, product_code, quantity)
        Purchase.add_purchase(purchase)

        purchase = Purchase.get_purchase(purchase_date, product_code)

        self.assertEqual(purchase.product_code, product_code, f"should be {product_code}")
        self.assertEqual(purchase.quantity, quantity)
        self.assertEqual(purchase.garment_name, garment_name)


if __name__ == '__main__':
    unittest.main()
