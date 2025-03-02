from sqlalchemy import QueuePool, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# 创建数据库引擎（这里使用 SQLite 数据库）
engine = create_engine(
    f"sqlite:///data.db",
    echo=False,
)

# 创建基础类
Base = declarative_base()

# 创建一个全局的 session
Session = scoped_session(sessionmaker(bind=engine))

# 在 Base 上定义 query_property
# Base.query = Session.query_property()
