from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, func, desc, and_

from sshp.models import Base
from sshp.models.Product import Product


class Sales(Base.dec_base):
    __tablename__ = 'sales'
    sales_id = Column(Integer(), primary_key=True)
    sales_date = Column(DateTime, default=datetime.now())
    bill_number = Column(Integer(), ForeignKey('billing.bill_number'))
    product_code = Column(String(15), ForeignKey('products.product_code'))
    quantity = Column(Integer(), nullable=False)
    amount = Column(Float(5, 2), nullable=False)

    def __repr__(self):
        return f'sales {self.bill_number}'

    @classmethod
    def get_sales(cls, bill_number):
        return Base.session.query(cls).filter_by(bill_number=bill_number).all()

    @staticmethod
    def add_sales(sale):
        sales_date, bill_number, product_code, quantity, amount = sale

        sale = Sales(sales_date=sales_date, bill_number=bill_number, product_code=product_code, quantity=quantity,
                     amount=amount)
        Base.session.add(sale)
        Base.session.commit()

    def delete_sales(self, bill_number):
        sales = self.get_sales(bill_number)

        if sales:
            for sale in sales:
                Base.session.delete(sale)
                Base.session.commit()
        else:
            print(f"bill_number '{bill_number}' not found in db!")

    @classmethod
    def sales_report_daily(cls):
        return Base.session.query(func.strftime('%d-%m-%Y', Sales.sales_date).label("sales_date"),
                                  Sales.product_code,
                                  func.sum(Sales.quantity).label("quantity")
                                  ).group_by(
            func.strftime('%d-%m-%Y', Sales.sales_date),
            Sales.product_code
        ).all()  # .having(func.strftime('%d-%m-%Y', Sales.sales_date) == sales_date)

    @classmethod
    def sales_report_monthly(cls):
        return Base.session.query(func.strftime('%m-%Y', Sales.sales_date).label("sales_month"),
                                  Sales.product_code,
                                  func.sum(Sales.quantity).label("quantity")
                                  ).group_by(
            func.strftime('%m-%Y', Sales.sales_date),
            Sales.product_code
        ).all()

    @classmethod
    def get_all_sales(cls):
        return Base.session.query(Sales, Product).outerjoin(Product).order_by(desc(Sales.sales_date)).all()

    @classmethod
    def get_bill_number_list(cls):
        return Base.session.query(Sales.bill_number).distinct().all()

    @classmethod
    def search_bill_number(cls, bill_number):
        return Base.session.query(Sales, Product).outerjoin(Product).filter(
            Sales.bill_number == bill_number) \
            .order_by(desc(cls.sales_date)).all()

    @classmethod
    def get_sales_data(cls, from_date, to_date):
        return Base.session.query(func.sum(cls.quantity), func.round(func.sum(cls.amount), 2)).filter(and_(
            func.strftime('%Y-%m-%d', Sales.sales_date) >= from_date,
            func.strftime('%Y-%m-%d', Sales.sales_date) <= to_date)).first()

    @classmethod
    def search_product_code(cls, product_code, from_date=None, to_date=None):
        if from_date and to_date:
            return Base.session.query(Sales, Product).outerjoin(Product).filter(and_(
                func.strftime('%Y-%m-%d', Sales.sales_date) >= from_date,
                func.strftime('%Y-%m-%d', Sales.sales_date) <= to_date,
                Sales.product_code == product_code))\
                .order_by(desc(cls.sales_date)).all()
        else:
            return Base.session.query(Sales, Product).outerjoin(Product).filter(
                Sales.product_code == product_code) \
                .order_by(desc(cls.sales_date)).all()

    @classmethod
    def search_sales(cls, from_date=None, to_date=None, product_name="", product_type="", product_size="",
                     selling_price=0.0):
        if from_date and to_date:
            if selling_price > 0:
                return Base.session.query(Sales, Product).outerjoin(Product).filter(and_(
                    func.strftime('%Y-%m-%d', Sales.sales_date) >= from_date,
                    func.strftime('%Y-%m-%d', Sales.sales_date) <= to_date,
                    Product.product_name.like(f'%{product_name}%'),
                    Product.product_type.like(f'%{product_type}%'),
                    Product.product_size.like(f'{product_size}%'),
                    # removed % in-front to prevent XXL while searching XL
                    Product.selling_price == selling_price
                )).order_by(desc(cls.sales_date)).all()
            else:
                return Base.session.query(Sales, Product).outerjoin(Product).filter(and_(
                    func.strftime('%Y-%m-%d', Sales.sales_date) >= from_date,
                    func.strftime('%Y-%m-%d', Sales.sales_date) <= to_date,
                    Product.product_name.like(f'%{product_name}%'),
                    Product.product_type.like(f'%{product_type}%'),
                    Product.product_size.like(f'{product_size}%'),
                    # removed % in-front to prevent XXL while searching XL
                )).order_by(desc(cls.sales_date)).all()
        else:
            if selling_price > 0:
                return Base.session.query(Sales, Product).outerjoin(Product).filter(and_(
                    Product.product_name.like(f'%{product_name}%'),
                    Product.product_type.like(f'%{product_type}%'),
                    Product.product_size.like(f'{product_size}%'),
                    # removed % in-front to prevent XXL while searching XL
                    Product.selling_price == selling_price
                )).order_by(desc(cls.sales_date)).all()

            return Base.session.query(Sales, Product).outerjoin(Product).filter(and_(
                Product.product_name.like(f'%{product_name}%'),
                Product.product_type.like(f'%{product_type}%'),
                Product.product_size.like(f'{product_size}%'),  # removed % in-front to prevent XXL while searching XL
            )).order_by(desc(cls.sales_date)).all()
