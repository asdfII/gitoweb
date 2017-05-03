# -*- coding: utf-8 -*-

from sqlalchemy import (
    Column, CHAR, Integer, String, ForeignKey,
    exc
)
from sqlalchemy.orm import relationship, backref
from db.database import Base


class GitRepo(Base):
    __tablename__ = 'git_repo'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    def __unicode__(self):
        return '<GitRepo %s>' % (self.name)


class GitGroup(Base):
    __tablename__ = 'git_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    git_repo_id = Column(Integer, ForeignKey('git_repo.id'))
    
    git_repo = relationship('GitRepo', backref=
        backref('git_group', lazy='dynamic')
    )
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    def __unicode__(self):
        return '<GitGroup %s>' % (self.name)


class GitUser(Base):
    __tablename__ = 'git_user'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    git_group_id = Column(Integer, ForeignKey('git_group.id'))
    
    git_group = relationship('GitGroup', backref=
        backref('git_user', lazy='dynamic')
    )
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    def __unicode__(self):
        return '<GitUser %s>' % (self.name)
