from sqlalchemy import Column, Integer, String
from sqlalchemy import func

from sshp.models import Base


class LkpProductSize(Base.dec_base):
    __tablename__ = 'lkp_product_size'

    lkp_id = Column(Integer(), primary_key=True)
    product_size = Column(String(25), nullable=False, unique=True)
    code = Column(String(2), nullable=False, unique=True)

    def __repr__(self):
        return f'product_size: {self.product_size}'

    @classmethod
    def get_product_size(cls, code):
        return Base.session.query(cls.product_size).filter_by(code=code).first()

    @classmethod
    def get_code(cls, product_size):
        return Base.session.query(cls.code).filter_by(product_size=product_size).scalar()

    @classmethod
    def get_next_code(cls, product_size):
        product_size_code = cls.get_code(product_size=product_size)

        if product_size_code:
            return product_size_code

        code = Base.session.query(func.max(cls.code)).scalar()
        if code:
            return int(code) + 1

        return 1

    @classmethod
    def get_all_product_sizes(cls):
        return Base.session.query(cls).all()

    @classmethod
    def create_lookup(cls, product_size):
        code = cls.get_next_code(product_size)
        product_size_lkp = cls(product_size=product_size, code=code)
        Base.session.add(product_size_lkp)
        Base.session.commit()

        return code

    @classmethod
    def delete_lookup(cls, product_size):
        product_size_lkp = Base.session.query(cls).filter_by(product_size=product_size).first()

        if product_size_lkp:
            Base.session.delete(product_size_lkp)
            Base.session.commit()
        else:
            print(f"product_size: '{product_size}' not found in db!")

    @classmethod
    def update_lookup_by_code(cls, product_size, code):
        product_size_lkp = Base.session.query(cls).filter_by(code=code).first()

        if product_size_lkp:
            product_size_lkp.product_size = product_size
            Base.session.commit()
        else:
            print(f"code: '{code}' not found in db!")

    @classmethod
    def update_lookup_by_product_size(cls, product_size, code):
        product_size_lkp = Base.session.query(cls).filter_by(product_size=product_size).first()

        if product_size_lkp:
            product_size_lkp.code = code
            Base.session.commit()
        else:
            print(f"product_size: '{product_size}' not found in db!")
