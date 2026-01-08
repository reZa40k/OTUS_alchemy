import os
from sqlalchemy import (
    MetaData,
    String,
    Text,
    ForeignKey,
)

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)

import config


PG_CONN_URI = (
    os.environ.get("SQLALCHEMY_PG_CONN_URI")
    or "postgresql+asyncpg://postgres:password@localhost/postgres"
)
# Base = None


async_engine = create_async_engine(
    url=PG_CONN_URI,
    echo=config.db_echo,
    pool_size=config.sqla_pool_size,
    max_overflow=config.sqla_max_overflow,
)

Session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"


class IdIntPkMixin:
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )


class User(IdIntPkMixin, Base):
    username: Mapped[str] = mapped_column(
        String(32),
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        default="",
        server_default="",
    )
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r}, email={self.email!r}, full_name={self.name!r})"

    def __repr__(self) -> str:
        return str(self)


class Post(IdIntPkMixin, Base):
    title: Mapped[str] = mapped_column(
        String(100),
    )
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
    )
    user: Mapped["User"] = relationship(
        back_populates="posts",
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r}, user_id={self.user_id!r})"

    def __repr__(self) -> str:
        return str(self)
