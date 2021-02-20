from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy import desc

from sshp.models import Base
from sshp.models.Stock import Stock


class StockTimeline(Base.dec_base):
    __tablename__ = 'stock_timeline'

    timeline_id = Column(Integer(), primary_key=True, autoincrement=True)
    entry_date = Column(DateTime, default=datetime.now())
    product_code = Column(String(25), ForeignKey('products.product_code'), primary_key=True)
    activity = Column(String(15), nullable=False)
    change = Column(String(5), nullable=False)
    available = Column(Integer(), nullable=False)

    def __repr__(self):
        return f'StockTimeline {self.product_code}'

    @classmethod
    def get_timeline(cls, product_code):
        return Base.session.query(cls).filter_by(product_code=product_code).order_by(desc(cls.timeline_id)).all()

    @classmethod
    def add_timeline(cls, entry_date, product_code, activity, change):
        stock = Stock.get_stock(product_code=product_code)

        new_timeline = StockTimeline(entry_date=entry_date, product_code=product_code, activity=activity,
                                     change=change, available=stock.quantity)

        Base.session.add(new_timeline)
        Base.session.commit()

        return Base.session.query(cls).filter_by(product_code=product_code).all()
