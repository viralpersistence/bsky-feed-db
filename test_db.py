from server.utils import get_or_add_user
from server.database import session, UserFollows, FeedUser, Post
import sqlalchemy

my_did = 'did:plc:ptqbnzqvblvezfga4zpqocu4'

'''
stmt = sqlalchemy.select(FeedUser).filter(FeedUser.did == my_did)
rows = session.execute(stmt).fetchone()

if rows:
    print('here0')
    user_id = rows[0].id
else:
    print('here1')
    user_id = add_user(my_did)
'''

user = get_or_add_user(my_did)
user_id = user.id
print(user_id)

# select * from posts join userfollows on posts.did=userfollows.follows_did where userfollows.userid=[my_userid]

#sqlalchemy.select(Post).where(Post.did.in_(all_followed_dids)).order_by(Post.indexed_at.desc()).limit(limit)
stmt = sqlalchemy.select(Post).join(UserFollows, Post.did == UserFollows.follows_did).where(UserFollows.user_id == user_id).order_by(Post.indexed_at.desc()).limit(10)
print(stmt)
posts = session.scalars(stmt).all()
print(posts)