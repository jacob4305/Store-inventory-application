from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///inventory.db')
Session = sessionmaker(bind=engine)
session = Session()

class Product(Base):
	__tablename__ = 'products'

	product_id = Column(Integer, primary_key=True)
	product_name = Column(String)
	product_quantity = Column(Integer)
	product_price = Column(Integer)
	date_updated = Column(DateTime)


