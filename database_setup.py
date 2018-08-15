import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
      return {
              'id': self.id,
              'name': self.name,

        }


class Items(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Category, backref=backref('item', cascade='all, delete'))


    @property
    def serialize(self):
        return {
                 'id'         : self.id,
               'name'         : self.name,
               'description'  : self.description,
               'categories'   : self.categories.name
           }

engine = create_engine('sqlite:///catalogitem.db')


Base.metadata.create_all(engine)
