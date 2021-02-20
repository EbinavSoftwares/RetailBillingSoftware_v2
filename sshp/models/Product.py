from datetime import date

from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from sqlalchemy import and_

from sshp.models import Base


class Product(Base.dec_base):
    __tablename__ = 'products'

    product_id = Column(Integer(), primary_key=True)
    product_code = Column(String(15), nullable=False)
    product_name = Column(String(25), nullable=False)
    product_type = Column(String(25))
    product_size = Column(String(25))
    selling_price = Column(Float(5, 2), nullable=False)
    actual_price = Column(Float(5, 2))
    added_date = Column(Date, default=date.today())
    is_active = Column(Boolean, unique=False, default=True)
    modified_date = Column(Date, default=date.today())

    def __repr__(self):
        return f'product: {Product}'

    @classmethod
    def get_product(cls, product_code):
        return Base.session.query(cls).filter_by(product_code=product_code).first()

    @classmethod
    def get_product_by_code(cls, product_code):
        return Base.session.query(cls).filter_by(product_code=product_code).first()
        # return Base.session.query(cls).filter(cls.product_code.like(f"{p_code}")).all()

    @classmethod
    def get_all_products(cls):
        return Base.session.query(cls).order_by(cls.product_code).all()

    @classmethod
    def get_active_products(cls):
        return Base.session.query(cls).filter_by(is_active=True).order_by(cls.product_code).all()

    @classmethod
    def get_inactive_products(cls):
        return Base.session.query(cls).filter_by(is_active=False).order_by(cls.product_code).all()

    @classmethod
    def get_product_name_list(cls):
        return Base.session.query(cls.product_name).filter_by(is_active=True).distinct()\
            .order_by(cls.product_name).all()

    @classmethod
    def get_product_type_list(cls):
        return Base.session.query(cls.product_type).distinct().all()

    @classmethod
    def get_product_size_list(cls):
        return Base.session.query(cls.product_size).distinct().all()

    @classmethod
    def get_product_sell_price_list(cls):
        return Base.session.query(cls.selling_price).distinct().all()

    @classmethod
    def get_product_status(cls, product_code):
        return Base.session.query(Product.is_active).filter(Product.product_code == product_code).scalar()

    @classmethod
    def search_products(cls, product_code=None, product_name="", product_type="", product_size="", selling_price=0.0):
        if product_code:
            return cls.get_product_by_code(product_code)

        if selling_price > 0:
            return Base.session.query(cls).filter(and_(
                Product.product_name.like(f'%{product_name}%'),
                Product.product_type.like(f'%{product_type}%'),
                Product.product_size.like(f'{product_size}%'),  # removed % in-front to prevent XXL while searching XL
                Product.selling_price == selling_price,
                Product.is_active
            )).order_by(cls.product_code).all()

        return Base.session.query(cls).filter(and_(
            Product.product_name.like(f'%{product_name}%'),
            Product.product_type.like(f'%{product_type}%'),
            Product.product_size.like(f'{product_size}%'),  # removed % in-front to prevent XXL while searching XL
            Product.is_active
        )).order_by(cls.product_code).all()

    @classmethod
    def add_product(cls, product):
        product_code, product_name, product_type, product_size, selling_price, actual_price = product

        product = Product(product_code=product_code, product_name=product_name, product_type=product_type,
                          product_size=product_size, selling_price=selling_price, actual_price=actual_price)
        Base.session.add(product)
        Base.session.commit()

        from sshp.models.Stock import Stock
        stock = (product_code, 0)
        Stock.add_stock(stock)

    @classmethod
    def delete_product_by_code(cls, product_code):
        product = cls.get_product(product_code=product_code)

        if product:
            Base.session.delete(product)
            Base.session.commit()
        else:
            print(f"product_code '{product_code}' not found in db!")

    @classmethod
    def deactivate_product(cls, product_code):
        product = cls.get_product(product_code=product_code)

        if product:
            product.is_active = False

            Base.session.commit()
        else:
            print(f"product_code '{product_code}' not found in db!")

    @classmethod
    def activate_product(cls, product_code):
        product = cls.get_product(product_code=product_code)

        if product:
            product.is_active = True

            Base.session.commit()
        else:
            print(f"product_code '{product_code}' not found in db!")

    @classmethod
    def update_product(cls, product):
        product_code, product_name, product_type, product_size, selling_price, actual_price = product

        product = cls.get_product(product_code=product_code)

        if product:
            product.product_name = product_name
            product.product_type = product_type
            product.product_size = product_size
            product.selling_price = selling_price
            product.actual_price = actual_price
            Base.session.commit()
        else:
            print(f"product_code '{product_code}' not found in db!")

    @classmethod
    def delete_product_entry(cls, product_code):
        my_product = cls.get_product(product_code)

        if my_product:
            Base.session.query(cls).filter_by(product_code=product_code).delete()
            Base.session.commit()
