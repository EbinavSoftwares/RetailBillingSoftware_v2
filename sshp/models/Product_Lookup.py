from datetime import date

from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from sqlalchemy import and_

from sshp.models import Base


class Product_Lookup(Base.dec_base):
    __tablename__ = 'product_lookup'

    lkp_id = Column(Integer(), primary_key=True)
    product_code_old = Column(Integer(), nullable=False)
    product_code_new = Column(String(15), nullable=False)

    def __repr__(self):
        return f'product: {Product_Lookup}'

    @classmethod
    def get_product(cls, product_code_old):
        return Base.session.query(cls).filter_by(product_code_old=product_code_old).first()

    @classmethod
    def get_product_by_code(cls, product_code_old):
        return Base.session.query(cls).filter_by(product_code_old=product_code_old).first()
