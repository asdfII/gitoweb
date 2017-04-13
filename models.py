# -*- coding: utf-8 -*-

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    exc
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GitUser(Base):
    __tablename__ = 'git_user'
    id = Column(String(20), primary_key=True)
    name = Column(String(20))


class GitGroup(Base):
    __tablename__ = 'git_group'
    id = Column(String(20), primary_key=True)
    name = Column(String(20))


class GitRepo(Base):
    __tablename__ = 'git_repo'
    id = Column(String(20), primary_key=True)
    name = Column(String(20))


class GitAuth(Base):
    __tablename__ = 'git_auth'
    id = Column(String(20), primary_key=True)
    name = Column(String(20))



def init_db(user, passwd, dbname, host='localhost', port=3306):
    engine = create_engine(
        "mysql+pymysql://%s:%s@%s:%s/%s" % (user, passwd, host, port, dbname)
        #~ "postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]"
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    session.close()


class DBOps(object):
    def __init__(self, dbname, dbuser, dbpass, dbhost='localhost', dbport=3306):
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbhost = dbhost
        self.dbport = dbport
    
    def connection(self):
        engine = create_engine(
            "mysql+pymysql://%s:%s@%s:%s/%s" % (dbuser, dbpass, dbhost, dbport, dbname)
        )