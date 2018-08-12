import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Items(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Category)


    @property
    def serialize(self):
        return {
               'name'         : self.name,
               'description'  : self.description,
               'id'         : self.id,
           }

engine = create_engine('sqlite:///catalogitem.db')


Base.metadata.create_all(engine)
