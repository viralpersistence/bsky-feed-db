import datetime
import sqlalchemy
from server.database import session, Post

cutoff = datetime.datetime.today() - datetime.timedelta(days=21)
stmt = sqlalchemy.delete(Post).where(Post.indexed_at < cutoff)
session.execute(stmt)