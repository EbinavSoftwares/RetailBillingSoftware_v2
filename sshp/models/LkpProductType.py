from sqlalchemy import Column, Integer, String
from sqlalchemy import func

from sshp.models import Base


class LkpProductType(Base.dec_base):
    __tablename__ = 'lkp_product_type'

    lkp_id = Column(Integer(), primary_key=True)
    product_type = Column(String(25), nullable=False, unique=True)
    code = Column(String(2), nullable=False, unique=True)

    def __repr__(self):
        return f'product_type: {self.product_type}'

    @classmethod
    def get_product_type(cls, code):
        return Base.session.query(cls.product_name).filter_by(code=code).first()

    @classmethod
    def get_code(cls, product_type):
        return Base.session.query(cls.code).filter_by(product_type=product_type).scalar()

    @classmethod
    def get_next_code(cls, product_type):
        product_type_code = cls.get_code(product_type=product_type)

        if product_type_code:
            return product_type_code

        code = Base.session.query(func.max(cls.code)).scalar()
        if code:
            return int(code) + 1

        return 1

    @classmethod
    def get_all_product_types(cls):
        return Base.session.query(cls).distinct().all()

    @classmethod
    def create_lookup(cls, product_type):
        code = cls.get_next_code(product_type)
        product_type_lkp = cls(product_type=product_type, code=code)
        Base.session.add(product_type_lkp)
        Base.session.commit()

        return code

    @classmethod
    def delete_lookup(cls, product_type):
        product_type_lkp = Base.session.query(cls).filter_by(product_type=product_type).first()

        if product_type_lkp:
            Base.session.delete(product_type_lkp)
            Base.session.commit()
        else:
            print(f"product_type: '{product_type}' not found in db!")

    @classmethod
    def update_lookup_by_code(cls, product_type, code):
        product_type_lkp = Base.session.query(cls).filter_by(code=code).first()

        if product_type_lkp:
            product_type_lkp.product_type = product_type
            Base.session.commit()
        else:
            print(f"code: '{code}' not found in db!")

    @classmethod
    def update_lookup_by_product_type(cls, product_type, code):
        product_type_lkp = Base.session.query(cls).filter_by(product_type=product_type).first()

        if product_type_lkp:
            product_type_lkp.code = code
            Base.session.commit()
        else:
            print(f"product_type: '{product_type}' not found in db!")
