# -*- coding: utf-8 -*-

from db.database import init_db, db_session
from index.models import GitUser, GitGroup, GitRepo
init_db()


#~ u = GitUser('admin')
#~ db_session.add(u)
#~ db_session.commit()
#~ for i in db_session.query(GitUser).all():
    #~ db_session.delete(i)
#~ db_session.commit()