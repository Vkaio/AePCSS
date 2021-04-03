from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base
from .object import Object

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(20))
    password = Column(String(80), nullable=False)
    create_date = Column(DateTime, default=func.now())

    objects = relationship(Object)    

    def __repr__(self):
        return f'User {self.name}'

    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'password': self.passowrd,
            'create_date': self.create_date
        }
