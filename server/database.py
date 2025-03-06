from datetime import datetime
import sqlitecloud
from server import config
import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

Base = declarative_base()

class Post(Base):
    __tablename__ = "post"

    id = Column("id", Integer, nullable=False, primary_key=True)
    uri = Column("uri", String, index=True, nullable=False)
    cid = Column("cid", String, nullable=False)
    did = Column("did", String, nullable=False)
    reply_parent = Column("reply_parent", String)
    reply_root = Column("reply_root", String)
    discoverable = Column("discoverable", Boolean, nullable=False, default=False)
    has_link = Column("has_link", Boolean, nullable=False, default=False)
    indexed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    #created_at = Column(DateTime, nullable=False)


class SubscriptionState(Base):
    __tablename__ = 'subscriptionstate'

    id = Column("id", Integer, nullable=False, primary_key=True)
    service = Column("service", String, nullable=False, unique=True)
    cursor = Column("cursor", Integer, nullable=False)


class FeedUser(Base):
    __tablename__ = 'feeduser'

    id = Column("id", Integer, nullable=False, primary_key=True)
    did = Column("did", String, index=True, nullable=False, unique=True)
    #discoverable = Column("discoverable", Boolean, nullable=False, default=False)

    replies_off = Column("replies_off", Boolean, nullable=False, default=False)


class UserFollows(Base):
    __tablename__ = 'userfollows'

    id = Column("id", Integer, nullable=False, primary_key=True)

    user_id = Column("user_id", Integer, ForeignKey(FeedUser.id), nullable=False)
    #did = Column("did", String, index=True, nullable=False)

    follows_did = Column("follows_did", String, nullable=False)
    uri = Column("uri", String, index=True, nullable=False)


'''
class UserListPost(Base):
    __tablename__ = "userlistpost"

    id = Column("id", Integer, nullable=False, primary_key=True)
    uri = Column("uri", String, index=True, nullable=False)
    cid = Column("cid", String, nullable=False)
    did = Column("did", String, nullable=False)
    #reply_parent = Column("reply_parent", String)
    #reply_parent_did = Column("reply_parent_did", String)
    #reply_root = Column("reply_root", String)
    #reply_root_did = Column("reply_root_did", String)
    indexed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
'''


'''
class DatabaseUser(Base):
    __tablename__ = 'dbuser'

    id = Column("id", Integer, nullable=False, primary_key=True)
    did = Column("did", String, index=True, nullable=False, unique=True)
    password = Column("password", String, nullable=False, unique=True)
'''

class UserList(Base):
    __tablename__ = 'userlist'

    id = Column("id", Integer, nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey(FeedUser.id), nullable=False)
    subscribes_to_did = Column("subscribes_to_did", String, nullable=False)

'''
class UserSetting(Base):
    __tablename__ = 'usersetting'

    id = Column("id", Integer, nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey(FeedUser.id), nullable=False)
    setting_name = Column("setting_name", String, nullable=False)
    setting_value = Column("setting_value", Boolean, nullable=False, default=False)
'''

class Feed(Base):
    __tablename__ = 'feed'

    id = Column("id", Integer, nullable=False, primary_key=True)
    feed_name = Column("feed_name", String, nullable=False, unique=True)


class FeedMember(Base):

    __tablename__ = 'feedmember'

    id = Column("id", Integer, nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey(FeedUser.id), nullable=False)
    feed_id = Column("feed_id", Integer, ForeignKey(Feed.id), nullable=False)



'''
class Follows(Base):
    __tablename__ = 'follows'

    id = Column("id", Integer, nullable=False, primary_key=True)
    did = Column("did", String, ForeignKey(User.did), index=True, nullable=False)
    follows_did = Column("follows_did", String, nullable=False)
'''

all_table_names = (
    "post",
    "subscriptionstate",
    "feeduser",
    "userfollows",
    #"userlistpost",
    "userlist",
    "feed",
    "feedmember"
)


engine = sqlalchemy.create_engine(config.SQLITE_CONN_STRING)
Session = sessionmaker(bind=engine)
session = Session()

#if not all([sqlalchemy.inspect(engine).has_table(table_name) for table_name in ("subscriptionstate","post","user","follows")]):
if not all([sqlalchemy.inspect(engine).has_table(table_name) for table_name in all_table_names]):
    Base.metadata.create_all(engine)

#print(sqlalchemy.inspect(engine).has_table("post"))
#print(sqlalchemy.inspect(engine).has_table("subscriptionstate"))

'''
if __name__ == '__main__':
    # drop tables
    Post.__table__.drop(engine)
    SubscriptionState.__table__.drop(engine)
    Follows.__table__.drop(engine)
    User.__table__.drop(engine)
'''
