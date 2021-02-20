from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sshp.models.Billing import Billing
from sshp.models.LkpProductName import LkpProductName
from sshp.models.LkpProductSize import LkpProductSize
from sshp.models.LkpProductType import LkpProductType
from sshp.models.Product import Product
from sshp.models.Purchase import Purchase
from sshp.models.Sales import Sales
from sshp.models.Stock import Stock
from sshp.models.StockTimeline import StockTimeline

engine = create_engine('sqlite:///../data/database.db')
Session = sessionmaker(bind=engine)
session = Session()

engine.execute("DELETE FROM sqlite_sequence")
session.commit()

session.query(Stock).delete()
session.commit()

session.query(StockTimeline).delete()
session.commit()

session.query(Sales).delete()
session.commit()

session.query(Purchase).delete()
session.commit()

session.query(Product).delete()
session.commit()

session.query(LkpProductType).filter(LkpProductType.code != '100').delete()
session.commit()

session.query(LkpProductSize).filter(and_(LkpProductSize.code != '10', LkpProductSize.code != '11')).delete()
session.commit()

session.query(LkpProductName).delete()
session.commit()

session.query(Billing).delete()
session.commit()
