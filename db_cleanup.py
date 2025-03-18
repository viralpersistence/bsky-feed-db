import datetime
import sqlalchemy
from server.database import db, Post

cutoff = datetime.datetime.today() - datetime.timedelta(days=3)
#stmt = sqlalchemy.delete(Post).where(Post.indexed_at < cutoff)
#session.execute(stmt)
#session.commit()

num_posts = len(Post.select())
print(num_posts)

q = Post.delete().where(Post.indexed_at < cutoff)
q.execute()

num_posts = len(Post.select())
print(num_posts)