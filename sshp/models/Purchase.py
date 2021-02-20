from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, and_, desc, func

from sshp.models import Base
from sshp.models.Product import Product


class Purchase(Base.dec_base):
    __tablename__ = 'purchase'

    purchase_id = Column(Integer(), primary_key=True)
    purchase_date = Column(DateTime, default=datetime.now())
    garment_name = Column(String(25), nullable=False)
    product_code = Column(String(15), ForeignKey('products.product_code'), nullable=False)
    quantity = Column(Integer(), nullable=False)

    def __repr__(self):
        return f'purchase {self.purchase_id}'

    @classmethod
    def get_all_garment_name(cls):
        return Base.session.query(cls.garment_name).distinct().all()

    @classmethod
    def get_all_purchase(cls):
        return Base.session.query(Purchase, Product).outerjoin(Product) \
            .order_by(desc(Purchase.purchase_date)).all()

    @classmethod
    def get_purchase_by_product_code(cls, product_code, from_date=None, to_date=None):
        if from_date and to_date:
            return Base.session.query(Purchase, Product).outerjoin(Product).filter(and_(
                func.strftime('%Y-%m-%d', Purchase.purchase_date) >= from_date,
                func.strftime('%Y-%m-%d', Purchase.purchase_date) <= to_date,
                Product.product_code == product_code)).order_by(desc(cls.sales_date)).all()
        else:
            return Base.session.query(Purchase, Product).outerjoin(Product)\
                .filter(Product.product_code == product_code).order_by(desc(cls.purchase_date)).all()

    @classmethod
    def get_purchase(cls, purchase_date, product_code):
        return Base.session.query(cls).filter(and_(func.strftime('%Y-%m-%d', Purchase.purchase_date) == purchase_date,
                                                   Purchase.product_code == product_code)).first()

    @classmethod
    def get_purchase_summary(cls, purchase_date, garment_name):
        return Base.session.query(Purchase, Product).outerjoin(Product).filter(and_(
            func.strftime('%Y-%m-%d', cls.purchase_date) == purchase_date,
            cls.garment_name == garment_name)).order_by(cls.product_code).all()

    @classmethod
    def search_purchase(cls, from_date=None, to_date=None, product_code=None, garment_name="", product_name="",
                        product_type="", product_size="", selling_price=0.0):
        if from_date and to_date:
            if selling_price > 0:
                return Base.session.query(Purchase, Product).outerjoin(Product).filter(and_(
                    func.strftime('%Y-%m-%d', Purchase.purchase_date) >= from_date,
                    func.strftime('%Y-%m-%d', Purchase.purchase_date) <= to_date,
                    Purchase.product_code.like(f'%{product_code}%'),
                    Purchase.garment_name.like(f'%{garment_name}%'),
                    Product.product_name.like(f'%{product_name}%'),
                    Product.product_type.like(f'%{product_type}%'),
                    Product.product_size.like(f'{product_size}%'),
                    # removed % in-front to prevent XXL while searching XL
                    Product.selling_price == selling_price
                )).order_by(cls.product_code).all()

            return Base.session.query(Purchase, Product).outerjoin(Product).filter(and_(
                func.strftime('%Y-%m-%d', Purchase.purchase_date) >= from_date,
                func.strftime('%Y-%m-%d', Purchase.purchase_date) <= to_date,
                Purchase.product_code.like(f'%{product_code}%'),
                Purchase.garment_name.like(f'%{garment_name}%'),
                Product.product_name.like(f'%{product_name}%'),
                Product.product_type.like(f'%{product_type}%'),
                Product.product_size.like(f'{product_size}%'),  # removed % in-front to prevent XXL while searching XL
            )).order_by(cls.product_code).all()
        else:
            if selling_price > 0:
                return Base.session.query(Purchase, Product).outerjoin(Product).filter(and_(
                    Purchase.product_code.like(f'%{product_code}%'),
                    Purchase.garment_name.like(f'%{garment_name}%'),
                    Product.product_name.like(f'%{product_name}%'),
                    Product.product_type.like(f'%{product_type}%'),
                    Product.product_size.like(f'{product_size}%'),
                    # removed % in-front to prevent XXL while searching XL
                    Product.selling_price == selling_price
                )).order_by(cls.product_code).all()

            return Base.session.query(Purchase, Product).outerjoin(Product).filter(and_(
                Purchase.product_code.like(f'%{product_code}%'),
                Purchase.garment_name.like(f'%{garment_name}%'),
                Product.product_name.like(f'%{product_name}%'),
                Product.product_type.like(f'%{product_type}%'),
                Product.product_size.like(f'{product_size}%'),  # removed % in-front to prevent XXL while searching XL
            )).order_by(cls.product_code).all()

    @staticmethod
    def add_purchase(purchase):
        purchase_date, garment_name, product_code, quantity = purchase

        new_purchase = Purchase(purchase_date=purchase_date, garment_name=garment_name, product_code=product_code,
                                quantity=quantity)
        Base.session.add(new_purchase)
        Base.session.commit()

    def delete_purchase(self, purchase_date, product_code):
        purchase = self.get_purcahse(purchase_date, product_code)

        if purchase:
            Base.session.delete(purchase)
            Base.session.commit()
        else:
            print(f"purchase '{purchase_date, product_code}' not found in db!")

    def update_purchase(self, purchase):
        purchase_date, garment_name, product_code, quantity = purchase

        purchase = self.get_purcahse(purchase_date, product_code)

        if purchase:
            purchase.purchase_date = purchase_date
            purchase.garment_name = garment_name
            purchase.product_code = product_code
            purchase.quantity = quantity
            Base.session.commit()
        else:
            print(f"purchase '{purchase_date, product_code}' not found in db!")
