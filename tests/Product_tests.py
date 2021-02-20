import unittest
from datetime import date
from tkinter import messagebox

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sshp.models.Product import Product
from sshp.models.LkpProductName import LkpProductName


class TestPurchase(unittest.TestCase):
    engine = create_engine('sqlite:///../data/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # def test_get_product_status(self):
    #     product_code = "200-101-17-0130"
    #
    #     status = Product.get_product_status(product_code=product_code)
    #     self.assertEqual(True, status, f"should be {True}")

    def test_validate_product(self):
        product = LkpProductName.validate_product_name("Pant", "Mens")
        print(product.product_code)
        # if product:
        #     print(f"Product: '{product}' is already exists!")
        #     messagebox.showerror("SS Fashion Tuty", f"Product already exists!")

    # def test_get_active_products(self):
    #     products = Product.get_active_products()
    #
    #     stock_dict = dict()
    #     for product in products:
    #         if not stock_dict[product.product_name]:
    #             stock_dict[product.product_name] = {
    #
    #             }
    #
    #     print(stock_dict)

            #     if product.product_name in product_name:
            #     product_name.append(
            #         product.product_name
            #     )
            #     product_type.append(
            #         product.product_type
            #     )
            # product_size.append(
            #     product.product_size
            # )





if __name__ == '__main__':
    unittest.main()
