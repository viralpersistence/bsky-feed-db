from datetime import datetime
from server import config
import peewee
from flask_login import UserMixin

db = peewee.MySQLDatabase(config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD, host=config.DB_HOST, port=int(config.DB_PORT))


class BaseModel(peewee.Model):
    class Meta:
        database = db

class Post(BaseModel):
    uri = peewee.CharField(index=True)
    cid = peewee.CharField()
    did = peewee.CharField()
    reply_parent = peewee.CharField(null=True, default=None)
    reply_root = peewee.CharField(null=True, default=None)

    discoverable = peewee.BooleanField(default=False)
    has_link = peewee.BooleanField(default=False)
    link_only = peewee.BooleanField(default=False)
    userlist_only = peewee.BooleanField(default=False)
    subfeed_only = peewee.IntegerField(null=True)

    indexed_at = peewee.DateTimeField(default=datetime.utcnow)


class SubscriptionState(BaseModel):
    service = peewee.CharField(unique=True)
    cursor = peewee.BigIntegerField()

class FeedUser(BaseModel):
    did = peewee.CharField(unique=True, index=True)
    replies_off = peewee.BooleanField(default=False)

class UserFollows(BaseModel):
    feeduser = peewee.ForeignKeyField(FeedUser, backref='follows')
    follows_did = peewee.CharField()
    follows_handle = peewee.CharField(null=True)
    follows_disp_name = peewee.CharField(null=True)

    uri = peewee.CharField(unique=True)

class UserList(BaseModel):
    feeduser = peewee.ForeignKeyField(FeedUser, backref='subscribes')
    subscribes_to_did = peewee.CharField()
    subscribes_to_handle = peewee.CharField()
    subscribes_to_disp_name = peewee.CharField()

class Subfeed(BaseModel):
    feed_name = peewee.CharField(unique=True)

class SubfeedMember(BaseModel):
    feeduser = peewee.ForeignKeyField(FeedUser, backref='subfeeds')
    subfeed = peewee.ForeignKeyField(Subfeed, backref='members')

class DbUser(UserMixin, BaseModel):
    feeduser = peewee.ForeignKeyField(FeedUser, backref='dbuser')
    password = peewee.CharField()

if db.is_closed():
    db.connect()
    db.create_tables([Post, SubscriptionState, FeedUser, UserFollows, UserList, Subfeed, SubfeedMember, DbUser])

'''
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
    uri = Column("uri", String(255), index=True, nullable=False)
    cid = Column("cid", String(255), nullable=False)
    did = Column("did", String(255), nullable=False)
    reply_parent = Column("reply_parent", String(255))
    reply_root = Column("reply_root", String(255))
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
    service = Column("service", String(255), nullable=False, unique=True)
    #cursor = Column("cursor", Integer, nullable=False)
    cursor = Column("cursor", String(255), nullable=False)


class FeedUser(Base):
    __tablename__ = 'feeduser'

    id = Column("id", Integer, nullable=False, primary_key=True)
    did = Column("did", String(255), index=True, nullable=False, unique=True)
    replies_off = Column("replies_off", Boolean, nullable=False, default=False)


class UserFollows(Base):
    __tablename__ = 'userfollows'

    id = Column("id", Integer, nullable=False, primary_key=True)

    user_id = Column("user_id", Integer, ForeignKey(FeedUser.id), nullable=False)
    #did = Column("did", String(255), index=True, nullable=False)

    follows_did = Column("follows_did", String(255), nullable=False)
    uri = Column("uri", String(255), index=True, nullable=False)


class UserList(Base):
    __tablename__ = 'userlist'

    id = Column("id", Integer, nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey(FeedUser.id), nullable=False)
    subscribes_to_did = Column("subscribes_to_did", String(255), nullable=False)



class Subfeed(Base):
    __tablename__ = 'subfeed'

    id = Column("id", Integer, nullable=False, primary_key=True)
    feed_name = Column("feed_name", String(255), nullable=False, unique=True)


class SubfeedMember(Base):
    __tablename__ = 'subfeedmember'

    id = Column("id", Integer, nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey(FeedUser.id), nullable=False)
    subfeed_id = Column("subfeed_id", Integer, ForeignKey(Subfeed.id), nullable=False)


all_table_names = (
    "post",
    "subscriptionstate",
    "feeduser",
    "userfollows",
    "userlist",
    "subfeed",
    "subfeedmember"
)


engine = sqlalchemy.create_engine(config.MYSQL_CONN_STRING)
Session = sessionmaker(engine)
session = Session()


if not all([sqlalchemy.inspect(engine).has_table(table_name) for table_name in all_table_names]):
    Base.metadata.create_all(engine)
'''