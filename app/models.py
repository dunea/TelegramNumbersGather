from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    SmallInteger,
    Float,
    BigInteger,
    Table,
    text, Index,
)

from app.database import Base


class ThreeEightsNumbers(Base):
    __tablename__ = 'three_eights_numbers'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(18), index=True, nullable=False)
