from fa_test.config import config
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(config['DB_URI'], convert_unicode=True)
metadata = MetaData()
session = scoped_session(sessionmaker(bind=engine))

def init_db(bind=engine):
    metadata.create_all(bind=bind)

def clear_db(bind=engine):
	metadata.drop_all(bind=bind)

from datetime import datetime
