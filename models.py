# -*- coding: utf-8 -*-

from sqlalchemy import (
    create_engine,
    Column,
    CHAR,
    Integer,
    String,
    exc
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GitUser(Base):
    __tablename__ = 'git_user'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))


class GitGroup(Base):
    __tablename__ = 'git_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))


class GitRepo(Base):
    __tablename__ = 'git_repo'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))


def init_db(dbuser, dbpass, dbname, dbhost='localhost', dbport=3306, dbtype='mysql'):
    global engine
    engine = create_engine(
        "mysql+pymysql://%s:%s@%s:%s/%s" % (dbuser, dbpass, dbhost, dbport, dbname)
    )
    if dbtype == 'postgresql':
        engine = create_engine(
            "postgresql+psycopg2://%s:%s@%s:%s/%s" % (dbuser, dbpass, dbhost, dbport, dbname)
        )
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    session.close()


init_db('gitolite', 'gitolite', 'gitolite')