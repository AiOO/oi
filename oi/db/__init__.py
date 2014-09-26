from .__secret__ import db_string
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(db_string, encoding='utf-8', echo=False)
Session = sessionmaker(bind=engine)

@contextmanager
def db_session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

