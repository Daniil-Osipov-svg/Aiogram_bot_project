from sqlalchemy import Float, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)

    age: Mapped[int] = mapped_column(Float(asdecimal=True), nullable=False)
    weight: Mapped[int] = mapped_column(Float(asdecimal=True), nullable=False)
    height: Mapped[int] = mapped_column(Float(asdecimal=True), nullable=False)
    gender: Mapped[str] = mapped_column(String(30), nullable=False)
    activity: Mapped[str] = mapped_column(String(30), nullable=False)