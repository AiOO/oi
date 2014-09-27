from oi.model import Base
from sqlalchemy import Column, Integer, Unicode, Table, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint

class Repository(Base):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True)
    github_id = Column(Integer, nullable=False)
    name = Column(Unicode, nullable=False)
    full_name = Column(Unicode, nullable=False)
    description = Column(Unicode, nullable=False)
    is_private = Column(Boolean, nullable=False)
    url = Column(Unicode, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    __table_args__ = (
            UniqueConstraint('github_id', name='uk_github_id'),
    )

