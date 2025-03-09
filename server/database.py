from datetime import datetime
#import sqlitecloud
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
    link_only = Column("link_only", Boolean, nullable=False, default=False)
    userlist_only = Column("userlist_only", Boolean, nullable=False, default=False)
    subfeed_only = Column("subfeed_only", Integer)
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
    replies_off = Column("replies_off", Boolean, nullable=False, default=False)


class UserFollows(Base):
    __tablename__ = 'userfollows'

    id = Column("id", Integer, nullable=False, primary_key=True)

    user_id = Column("user_id", Integer, ForeignKey(FeedUser.id), nullable=False)
    #did = Column("did", String, index=True, nullable=False)

    follows_did = Column("follows_did", String, nullable=False)
    uri = Column("uri", String, index=True, nullable=False)


class UserList(Base):
    __tablename__ = 'userlist'

    id = Column("id", Integer, nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey(FeedUser.id), nullable=False)
    subscribes_to_did = Column("subscribes_to_did", String, nullable=False)



class Subfeed(Base):
    __tablename__ = 'subfeed'

    id = Column("id", Integer, nullable=False, primary_key=True)
    feed_name = Column("feed_name", String, nullable=False, unique=True)


class SubfeedMember(Base):
    __tablename__ = 'subfeedmember'

    id = Column("id", Integer, nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey(FeedUser.id), nullable=False)
    subfeed_id = Column("subfeed_id", Integer, ForeignKey(Subfeed.id), nullable=False)

'''
class SubfeedPost(Base):
    __tablename__ = 'subfeedpost'

    id = Column("id", Integer, nullable=False, primary_key=True)
    post_id = Column("post_id", Integer, ForeignKey(Post.id), nullable=False)
    subfeed_id = Column("subfeed_id", Integer, ForeignKey(Subfeed.id), nullable=False)
'''


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
    "userlist",
    "subfeed",
    "subfeedmember"
)


db_path = '/home/yocissms/bsky-feed-db/test.db'
engine = sqlalchemy.create_engine("sqlite:///"+db_path)
Session = sessionmaker(engine)
session = Session()


'''
engine = sqlalchemy.create_engine(config.SQLITE_CONN_STRING)
Session = sessionmaker(bind=engine)
session = Session()
'''

if not all([sqlalchemy.inspect(engine).has_table(table_name) for table_name in all_table_names]):
    Base.metadata.create_all(engine)
