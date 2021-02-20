from sqlalchemy import Column, Integer, String
from sqlalchemy import func, and_

from sshp.models import Base
from sshp.models.ProductCategory import ProductCategory


class LkpProductName(Base.dec_base):
    __tablename__ = 'lkp_product_name'

    lkp_id = Column(Integer(), primary_key=True)
    product_name = Column(String(25), nullable=False, unique=True)
    product_category = Column(String(25), nullable=False)
    code = Column(String(3), nullable=False, unique=True)

    def __repr__(self):
        return f'product_name: {self.product_name}'

    @classmethod
    def get_product_name(cls, code):
        return Base.session.query(cls.product_name).filter_by(code=code).first()

    @classmethod
    def get_product_category(cls, product_name):
        return Base.session.query(cls.product_category).filter_by(product_name=product_name).scalar()

    @classmethod
    def get_product_name_short(cls, product_name):
        return Base.session.query(cls.product_name_short).filter_by(product_name=product_name).scalar()

    @classmethod
    def get_code(cls, product_name):
        return Base.session.query(cls.code).filter_by(product_name=product_name).scalar()

    @classmethod
    def validate_product_name(cls, product_name, product_category):
        return Base.session.query(cls).filter(
            and_(cls.product_name == product_name, cls.product_category == product_category)
        ).first()

    @classmethod
    def get_next_code(cls, product_category, product_name):
        product_name_code = cls.get_code(product_name=product_name)

        if product_name_code:
            return product_name_code

        code = Base.session.query(func.max(cls.code)).filter_by(product_category=product_category).scalar()
        if code:
            return int(code)+1

        return ProductCategory.get_start_num(category=product_category)

    @classmethod
    def get_all_product_names(cls):
        return Base.session.query(cls).distinct().all()

    @classmethod
    def create_lookup(cls, product_name, product_category):
        code = cls.get_next_code(product_category, product_name)
        product_name_lkp = cls(product_name=product_name, product_category=product_category, code=code)
        Base.session.add(product_name_lkp)
        Base.session.commit()

        return code

    @classmethod
    def delete_lookup(cls, product_name):
        product_name_lkp = Base.session.query(cls).filter_by(product_name=product_name).first()

        if product_name_lkp:
            Base.session.delete(product_name_lkp)
            Base.session.commit()
        else:
            print(f"product_name '{product_name}' not found in db!")

    @classmethod
    def update_lookup_by_code(cls, product_name, product_name_short, code):
        product_name_lkp = Base.session.query(cls).filter_by(code=code).first()

        if product_name_lkp:
            product_name_lkp.product_name = product_name
            product_name_lkp.product_name_short = product_name_short
            Base.session.commit()
        else:
            print(f"code '{code}' not found in db!")

    @classmethod
    def update_lookup_by_product_name(cls, product_name, product_name_short, code):
        product_name_lkp = Base.session.query(cls).filter_by(product_name=product_name).first()

        if product_name_lkp:
            product_name_lkp.code = code
            product_name_lkp.product_name_short = product_name_short
            Base.session.commit()
        else:
            print(f"product_name '{product_name}' not found in db!")
