# -*- coding: utf-8 -*-

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from gitoweb.settings import DATABASES


DRIVE = 'mysql+pymysql://'
if DATABASES['TYPE'] == 'postgresql':
    DRIVE = 'postgresql+psycopg2://'
engine = create_engine(
    DRIVE + DATABASES['USER'] + ':' + DATABASES['PASS']
    + '@' + DATABASES['HOST'] + ':' + DATABASES['PORT']
    + '/' + DATABASES['NAME'],
    convert_unicode=True
)
if DATABASES['TYPE'] == 'sqlite':
    DRIVE = 'sqlite://'
    engine = create_engine(
        DRIVE + '/' + os.path.dirname(os.path.abspath(__file__))
        + '/' + DATABASES['NAME'] + '.db',
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
    from index import models
    Base.metadata.create_all(bind=engine)
