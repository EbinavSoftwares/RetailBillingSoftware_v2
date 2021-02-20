from sqlalchemy import Column, Integer, ForeignKey, String, func
from sqlalchemy import and_

from sshp.models import Base
from sshp.models.Product import Product


class Stock(Base.dec_base):
    __tablename__ = 'stock'
    product_code = Column(String(15), ForeignKey('products.product_code'), primary_key=True)
    quantity = Column(Integer(), nullable=False)

    def __repr__(self):
        return f'Stock {self.product_code}'

    @classmethod
    def get_stock(cls, product_code):
        return Base.session.query(cls).filter_by(product_code=product_code).first()

    @classmethod
    def get_all_stocks(cls):
        return Base.session.query(Product, Stock).outerjoin(Stock).order_by(Product.product_code).all()

    @classmethod
    def get_all_active_stocks(cls):
        return Base.session.query(Product, Stock).outerjoin(Stock).filter(Product.is_active) \
                .order_by(Product.product_code).all()

    @classmethod
    def get_all_active_stocks_by_product_name(cls, product_name):
        return Base.session.query(Product, Stock).outerjoin(Stock).filter(and_(
            Product.is_active,
            Product.product_name == product_name))\
            .order_by(Product.product_code).all()

    @classmethod
    def get_active_product_name_summary(cls):
        return Base.session.query(Product.product_name,
                                  func.sum(cls.quantity).label('total_quantity')
                                  ).outerjoin(Stock) \
            .filter(Product.is_active) \
            .group_by(Product.product_name) \
            .order_by(Product.product_name).all()

    @classmethod
    def get_active_product_type_summary(cls, product_name):
        return Base.session.query(Product.product_type,
                                  func.sum(cls.quantity).label('total_quantity')
                                  ).outerjoin(Stock)\
            .filter(and_(Product.is_active, Product.product_name == product_name))\
            .group_by(Product.product_type) \
            .order_by(Product.product_type).all()

    @classmethod
    def get_active_stock_size_summary(cls, product_name):
        return Base.session.query(Product.product_size,
                                  func.sum(cls.quantity).label('total_quantity')
                                  ).outerjoin(Stock) \
            .filter(and_(Product.is_active, Product.product_name == product_name)) \
            .group_by(Product.product_size) \
            .order_by(Product.product_size).all()

    @classmethod
    def get_stocks_by_quantity(cls, quantity):
        return Base.session.query(Product, Stock).outerjoin(Stock).filter(Stock.quantity <= quantity) \
            .order_by(Product.product_code).all()

    @classmethod
    def get_total_stock_value(cls):
        return Base.session.query(func.sum(cls.quantity).label('total_quantity'),
                                  func.sum(Product.selling_price * cls.quantity).label('total_stock_value'))\
            .join(Product).first()

    @classmethod
    def get_stock_value_by_product(cls):
        return Base.session.query(Product.product_name,
                                  func.sum(cls.quantity).label('total_quantity'),
                                  func.sum(Product.selling_price * cls.quantity).label('total_stock_value'))\
            .join(Product).group_by(Product.product_name).all()

    @classmethod
    def search_stock(cls, product_code=None, product_name="", product_type="", product_size="", selling_price=0):
        if product_code:
            return Base.session.query(Product, Stock).outerjoin(Stock).filter(Product.product_code == product_code)\
                .order_by(Product.product_code).first()

        if selling_price > 0:
            return Base.session.query(Product, Stock).outerjoin(Stock).filter(and_(
                Product.product_name.like(f'%{product_name}%'),
                Product.product_type.like(f'%{product_type}%'),
                Product.product_size.like(f'%{product_size}%'),
                Product.selling_price == selling_price
            )).order_by(Product.product_code).all()

        return Base.session.query(Product, Stock).outerjoin(Stock).filter(and_(
            Product.product_name.like(f'%{product_name}%'),
            Product.product_type.like(f'%{product_type}%'),
            Product.product_size.like(f'%{product_size}%'),
        )).order_by(Product.product_code).all()

    @staticmethod
    def add_stock(stock):
        product_code, quantity = stock

        stock = Stock(product_code=product_code, quantity=quantity)
        Base.session.add(stock)
        Base.session.commit()

    @classmethod
    def clear_stock(cls, product_code):
        stock = cls.get_stock(product_code)

        if stock:
            print(f"product_code: '{product_code}' available stock: {stock.quantity} in db")
            stock.quantity = 0

            Base.session.commit()
        else:
            print(f"product_code: '{product_code}' not found in db!")

    @classmethod
    def upload_stock(cls, stock):
        product_code, quantity = stock

        my_stock = cls.get_stock(product_code)

        if my_stock:
            my_stock.quantity = my_stock.quantity + quantity

            Base.session.commit()

    @classmethod
    def compute_stock(cls, stock):
        product_code, quantity = stock

        my_stock = cls.get_stock(product_code)

        if my_stock:
            my_stock.quantity = my_stock.quantity - quantity

            Base.session.commit()

    @classmethod
    def update_stock(cls, stock):
        product_code, quantity = stock

        my_stock = cls.get_stock(product_code)

        if my_stock:
            my_stock.quantity = quantity
            Base.session.commit()
        else:
            cls.add_stock(stock)

    @classmethod
    def delete_stock_entry(cls, product_code):
        my_stock = cls.get_stock(product_code)

        if my_stock:
            Base.session.query(cls).filter_by(product_code=product_code).delete()
            Base.session.commit()
