from oi.model import Base
from sqlalchemy import Column, Integer, Unicode, ForeignKey, Float, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    google_id = Column(Unicode, nullable=False)
    name = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=False)
    avatar = Column(Unicode)
    __table_args__ = (
            UniqueConstraint('google_id', name='uk_google_id'),
    )

