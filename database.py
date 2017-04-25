# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dbparams import dbtype, dbname, dbuser, dbpass, dbhost, dbport


if dbtype == 'sqlite':
    dbtype = 'sqlite://'
    engine = create_engine(
        dbtype + '/gitolite.db',
        convert_unicode=True
    )
if dbtype == 'mysql':
    dbtype = 'mysql+pymysql://'
    engine = create_engine(
        dbtype + dbuser + ':' + dbpass + '@' + dbhost
        + ':' + dbport + '/' + dbname,
        convert_unicode=True
    )
elif dbtype == 'postgresql':
    dbtype = 'postgresql+psycopg2://'
    engine = create_engine(
        dbtype + dbuser + ':' + dbpass + '@' + dbhost
        + ':' + dbport + '/' + dbname,
        convert_unicode=True
    )

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
