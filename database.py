from datetime import datetime
import sqlitecloud
import config
import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

'''
# Open the connection to SQLite Cloud
conn = sqlitecloud.connect(config.SQLITE_CONN_STRING)


#if not post_table_exists:
conn.execute("""CREATE TABLE IF NOT EXISTS "post" ("id" INTEGER NOT NULL PRIMARY KEY, "uri" VARCHAR(255) NOT NULL, "cid" VARCHAR(255) NOT NULL, "reply_parent" VARCHAR(255), "reply_root" VARCHAR(255), "indexed_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);""")
conn.execute("""CREATE INDEX IF NOT EXISTS "post_uri" ON "post" ("uri");""")


#if not subscrptionstate_exists:
conn.execute("""CREATE TABLE IF NOT EXISTS "subscriptionstate" ("id" INTEGER NOT NULL PRIMARY KEY, "service" VARCHAR(255) NOT NULL, "cursor" INTEGER NOT NULL);""")
conn.execute("""CREATE UNIQUE INDEX IF NOT EXISTS "subscriptionstate_service" ON "subscriptionstate" ("service");""")

#print(post_table_exists)


conn.close()
'''

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
    #SubscriptionState.__table__.drop(engine)

'''
import peewee

db = peewee.SqliteDatabase('feed_database.db')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Post(BaseModel):
    uri = peewee.CharField(index=True)
    cid = peewee.CharField()
    reply_parent = peewee.CharField(null=True, default=None)
    reply_root = peewee.CharField(null=True, default=None)
    indexed_at = peewee.DateTimeField(default=datetime.utcnow)


class SubscriptionState(BaseModel):
    service = peewee.CharField(unique=True)
    cursor = peewee.BigIntegerField()


if db.is_closed():
    db.connect()
    db.create_tables([Post, SubscriptionState])
'''