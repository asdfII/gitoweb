# -*- coding: utf-8 -*-


# Insert
foo = MyModel(field1='value', field2='value')
session.add(foo)
session.commit()


# Delete
obj = MyModel.query.get(the_id)
session.delete(obj)
session.commit()


# Update
obj = MyModel.query.get(the_id)
obj.name = 'New Value'
session.commit()


# Primary Key Queries
obj = MyModel.query.get(the_id)


# General Query Syntax
>>> print MyModel.thread_count + MyModel.post_count + 1
(model.thread_count + model.post_count) + :param_1
>>> print MyModel.id.between(1, 10) & MyModel.name.startswith('a')
model.model_id BETWEEN :model_id_1 AND :model_id_2 AND
    model.name LIKE :name_1 || '%%'

active_users_with_a_or_b = User.query.filter(
    (User.name.startswith('a') | User.name.startswith('b')) &
    (User.is_active == True)
).all()


# Date Based Queries
from sqlalchemy.sql import extract

entries_a_month = Entry.query.filter(
    (extract(Entry.pub_date, 'year') == 2011) &
    (extract(Entry.pub_date, 'month') == 1)
).all()


# Sort
forwards = MyModel.query.order_by(MyModel.pub_date)
backwards = MyModel.query.order_by(MyModel.pub_date.desc())


# Aggregates
from sqlalchemy.sql import func

q = session.query(func.count(User.id))


# Joins
posts = Post.query.join(Author).filter(Author.name == the_author_name)


author_query = Author.query.filter(Author.name == the_author_name)
posts = Post.query.filter(Post.author_id.in_(author_query))
