from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from sqlalchemy import Integer, String

from app.database import Base


class ThreeEightsNumbers(Base):
    __tablename__ = "three_eights_numbers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(18), index=True, nullable=False)

    def __repr__(self) -> str:
        return f"ThreeEightsNumbers(id={self.id!r}, number={self.number!r})"
