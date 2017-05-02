# -*- coding: utf-8 -*-

from sqlalchemy import (
    create_engine,
    Column, CHAR, Integer, String,
    exc
)
from db.database import Base


class GitUser(Base):
    __tablename__ = 'git_user'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    def __unicode__(self):
        return '<GitUser %s>' % (self.name)


class GitGroup(Base):
    __tablename__ = 'git_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    def __unicode__(self):
        return '<GitGroup %s>' % (self.name)


class GitRepo(Base):
    __tablename__ = 'git_repo'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    def __unicode__(self):
        return '<GitRepo %s>' % (self.name)