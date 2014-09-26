from oi.model import *
from oi.db import engine

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

