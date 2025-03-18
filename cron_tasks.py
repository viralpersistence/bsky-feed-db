import datetime
import time
from server.database import db, Post, FeedUser
from server.utils import get_uf_handles

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

all_users = FeedUser.select()

for user in all_users:
    if user.dbuser:
        get_uf_handles(user)

    print(user.did)
    #get_uf_handles(user)
    #time.sleep(30)