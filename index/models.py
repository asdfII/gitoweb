# -*- coding: utf-8 -*-

from sqlalchemy import (
    Table,
    Column, CHAR, Integer, String, ForeignKey,
    exc
)
from sqlalchemy.orm import relationship, backref
from db.database import Base


association_table = Table('association', Base.metadata,
    Column('git_repo_id', Integer, ForeignKey('git_repo.id')),
    Column('git_group_id', Integer, ForeignKey('git_group.id')),
    Column('git_user_id', Integer, ForeignKey('git_user.id'))
)


class GitRepo(Base):
    __tablename__ = 'git_repo'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    
    git_group = relationship('GitGroup',
        secondary=association_table,
        backref=backref('git_repo', lazy='dynamic'),
        cascade='all, delete',
        order_by='GitGroup.id',
    )
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    def __unicode__(self):
        return '<GitRepo %s>' % (self.name)


class GitGroup(Base):
    __tablename__ = 'git_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    
    git_repo = relationship('GitRepo',
        secondary=association_table,
        backref=backref('git_group', lazy='dynamic'),
        cascade='all, delete',
        order_by='GitRepo.id',
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
    
    git_group = relationship('GitGroup',
        secondary=association_table,
        backref=backref('git_user', lazy='dynamic'),
        cascade='all, delete',
        order_by='GitGroup.id',
    )
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    def __unicode__(self):
        return '<GitUser %s>' % (self.name)
