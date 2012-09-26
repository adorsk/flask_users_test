from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker, class_mapper, aliased
from sqlalchemy.orm.properties import RelationshipProperty


engine = create_engine(
    'sqlite:////home/adorsk/projects/fa_test/db.sqlite', 
    convert_unicode=True
)
metadata = MetaData()
session = scoped_session(sessionmaker(bind=engine))

def init_db(bind=engine):
    metadata.create_all(bind=bind)

def clear_db(bind=engine):
	metadata.drop_all(bind=bind)
