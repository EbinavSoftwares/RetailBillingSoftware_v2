from sqlalchemy import Column, Integer, String, and_

from sshp.models import Base


class ProductCategory(Base.dec_base):
    __tablename__ = 'product_category'

    category_id = Column(Integer(), primary_key=True)
    category = Column(String(25), nullable=False, unique=True)
    start_num = Column(String(3), nullable=False, unique=True)
    end_num = Column(String(3), nullable=False, unique=True)

    def __repr__(self):
        return f'product_category: {ProductCategory}'

    @classmethod
    def get_category(cls, category):
        return Base.session.query(cls).filter_by(category=category).first()

    @classmethod
    def get_category_by_code(cls, code):
        return Base.session.query(cls.category).filter(
            and_(
                code >= cls.start_num,
                code <= cls.end_num)
        ).scalar()

    @classmethod
    def get_start_num(cls, category):
        return Base.session.query(cls.start_num).filter_by(category=category).scalar()

    @classmethod
    def get_all_categories(cls):
        return Base.session.query(cls).order_by(cls.start_num).all()

    @classmethod
    def add_category(cls, product_category):
        category, start_num, end_num = product_category

        product_category = ProductCategory(category=category, start_num=start_num, end_num=end_num)
        Base.session.add(product_category)
        Base.session.commit()

    @classmethod
    def update_category(cls, product_category):
        category, start_num, end_num = product_category

        product_category = cls.get_category(category)

        if product_category:
            product_category.start_num = start_num
            product_category.end_num = end_num

            Base.session.commit()
        else:
            print(f"product_category '{product_category}' not found in db!")
