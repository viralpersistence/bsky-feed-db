from datetime import datetime
import sqlitecloud
from server import config
import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Post(Base):
    __tablename__ = "post"

    id = Column("id", Integer, nullable=False, primary_key=True)
    uri = Column("uri", String, index=True, nullable=False)
    cid = Column("cid", String, nullable=False)
    reply_parent = Column("reply_parent", String)
    reply_root = Column("reply_root", String)
    indexed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class SubscriptionState(Base):
    __tablename__ = 'subscriptionstate'

    id = Column("id", Integer, nullable=False, primary_key=True)
    service = Column("service", String, nullable=False)
    cursor = Column("cursor", Integer, nullable=False)


engine = sqlalchemy.create_engine(config.SQLITE_CONN_STRING)
Session = sessionmaker(bind=engine)
session = Session()

if not (sqlalchemy.inspect(engine).has_table("post") and sqlalchemy.inspect(engine).has_table("subscriptionstate")):
    Base.metadata.create_all(engine)



#print(sqlalchemy.inspect(engine).has_table("post"))
#print(sqlalchemy.inspect(engine).has_table("subscriptionstate"))

if __name__ == '__main__':
    # drop tables
    Post.__table__.drop(engine)
    SubscriptionState.__table__.drop(engine)
