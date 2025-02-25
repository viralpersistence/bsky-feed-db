from datetime import datetime
import sqlitecloud
from server import config
import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

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
    indexed_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SubscriptionState(Base):
    __tablename__ = 'subscriptionstate'

    id = Column("id", Integer, nullable=False, primary_key=True)
    service = Column("service", String, nullable=False, unique=True)
    cursor = Column("cursor", Integer, nullable=False)

class User(Base):
    __tablename__ = 'user'

    id = Column("id", Integer, nullable=False, primary_key=True)
    did = Column("did", String, index=True, nullable=False, unique=True)
    #discoverable = Column("discoverable", Boolean, nullable=False, default=False)

'''
class Follows(Base):
    __tablename__ = 'follows'

    id = Column("id", Integer, nullable=False, primary_key=True)
    did = Column("did", String, ForeignKey(User.did), index=True, nullable=False)
    follows_did = Column("follows_did", String, nullable=False)
'''



engine = sqlalchemy.create_engine(config.SQLITE_CONN_STRING)
Session = sessionmaker(bind=engine)
session = Session()

#if not all([sqlalchemy.inspect(engine).has_table(table_name) for table_name in ("subscriptionstate","post","user","follows")]):
if not all([sqlalchemy.inspect(engine).has_table(table_name) for table_name in ("subscriptionstate","post","user")]):
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
