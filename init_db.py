# -*- coding: utf-8 -*-

from db.database import init_db, db_session
from index.models import GitUser, GitGroup, GitRepo
init_db()
