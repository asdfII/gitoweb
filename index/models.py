# -*- coding: utf-8 -*-

from sqlalchemy import (
    Table, Column, CHAR, Integer, String,
    ForeignKey, PrimaryKeyConstraint,
    exc
)
from sqlalchemy.orm import relationship, backref
from db.database import Base


asso_repo_group = Table('asso_repo_group', Base.metadata,
    Column('git_repo_id', Integer, ForeignKey('git_repo.id')),
    Column('git_group_id', Integer, ForeignKey('git_group.id')),
    PrimaryKeyConstraint('git_repo_id', 'git_group_id'),
)


asso_group_user = Table('asso_group_user', Base.metadata,
    Column('git_group_id', Integer, ForeignKey('git_group.id')),
    Column('git_user_id', Integer, ForeignKey('git_user.id')),
    PrimaryKeyConstraint('git_group_id', 'git_user_id'),
)


class GitRepo(Base):
    __tablename__ = 'git_repo'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return '<GitRepo %s>' % (self.name)


class GitGroup(Base):
    __tablename__ = 'git_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    
    git_repo = relationship('GitRepo',
        secondary=asso_repo_group,
        backref=backref('git_group', lazy='dynamic'),
    )
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return '<GitGroup %s>' % (self.name)


class GitUser(Base):
    __tablename__ = 'git_user'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    
    git_group = relationship('GitGroup',
        secondary=asso_group_user,
        backref=backref('git_user', lazy='dynamic'),
    )
    
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return '<GitUser %s>' % (self.name)


#~ class AssoUserRepo(Base):
    #~ __tablename__ = 'asso_user_repo'
    #~ git_user_id = Column(
        #~ Integer,
        #~ ForeignKey('git_user.id'), 
        #~ primary_key=True,
    #~ )
    #~ git_repo_id = Column(
        #~ Integer,
        #~ ForeignKey('git_repo.id'),
        #~ primary_key=True,
    #~ )
    #~ PrimaryKeyConstraint('git_user_id', 'git_repo_id')
    
    #~ def __init__(self, git_user_id, git_repo_id):
        #~ self.git_user_id = git_user_id
        #~ self.git_repo_id = git_repo_id
    
    #~ def __repr__(self):
        #~ return '<AssoUserRepo %s>' (self.__tablename__)
