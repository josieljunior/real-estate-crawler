from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lng = Column(Float)
    area = Column(Float)
    type = Column(String(255))
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    parking_spaces = Column(Integer)
    link = Column(String(255))
    address = Column(String(255))
    crawler = Column(String(255))
    created_date = Column(DateTime, default=func.now())

    prices = relationship("Price", back_populates="property")

class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    created_date = Column(DateTime, default=func.now())
    property_id = Column(Integer, ForeignKey('properties.id'))

    property = relationship("Property", back_populates="prices")
