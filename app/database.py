"""数据库引擎与会话工厂定义。"""

from sqlalchemy import Column, Integer, String, QueuePool, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.log import get_logger


logger = get_logger(__name__)

# 创建数据库引擎（这里使用 SQLite 数据库）
engine = create_engine(
    f"sqlite:///data.db",
    echo=False,
)
logger.info("数据库引擎已初始化，当前使用 SQLite 文件 data.db")

# 创建基础类
Base = declarative_base()

# 创建一个全局的 session
Session = scoped_session(sessionmaker(bind=engine))
logger.debug("数据库会话工厂已初始化")

# 在 Base 上定义 query_property
# Base.query = Session.query_property()
