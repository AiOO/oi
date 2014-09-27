from oi.model import Base
from sqlalchemy import Column, Integer, Unicode, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    google_id = Column(Unicode, nullable=False)
    github_access_token = Column(Unicode)
    name = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=False)
    avatar = Column(Unicode)
    repositories = relationship('Repository', backref='owner_user')
    __table_args__ = (
            UniqueConstraint('google_id', name='uk_google_id'),
            UniqueConstraint(
                'github_access_token',
                name='uk_github_access_token'
            ),
    )

