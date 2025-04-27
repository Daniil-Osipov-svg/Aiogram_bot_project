from sqlalchemy import Float, String, DateTime, func, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    tg_id = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)

    info = relationship('UserInfo', backref='user', uselist=False)
    dishes = relationship('Dish', backref='user')

class UserInfo(Base):
    __tablename__ = 'user_info'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'), unique=True)

    age: Mapped[int] = mapped_column(Float(asdecimal=True), nullable=False)
    weight: Mapped[int] = mapped_column(Float(asdecimal=True), nullable=False)
    height: Mapped[int] = mapped_column(Float(asdecimal=True), nullable=False)
    gender: Mapped[str] = mapped_column(String(30), nullable=False)
    activity: Mapped[str] = mapped_column(String(30), nullable=False)
    tdee: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=True)

class Dish(Base):
    __tablename__ = 'dishes'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'), nullable=False)
    dish_name: Mapped[str] = mapped_column(String(150), nullable=False)
    carbs: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    proteins: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    fats: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)