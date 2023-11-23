from typing import Annotated, Optional
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base, str_256


class AccountsData(Base):
    __tablename__ = "accounts"

    """ Variables
    
    :param user_id: primary key
    :param service: the user's selected service
    :param date_client: the user's selected date
    """

    user_id: Mapped[Annotated[int, mapped_column(unique=True, primary_key=True, nullable=False)]]
    service: Mapped[str_256]
    name: Mapped[str_256]
    surname: Mapped[str_256]
    date_client: Mapped[str_256]
    phone: Mapped[str_256]


class Dates(Base):
    __tablename__ = "dates"
    """ Variables

    :param user_id: primary key
    :param date_admin: a date that admin wrote
    """
    user_id: Mapped[Annotated[int, mapped_column(primary_key=True)]]
    date_admin: Mapped[str_256]


class AdminsData(Base):
    __tablename__ = "admins"

    """ Variables

    :param id: primary key
    :param user_id: Telegram user_id
    """

    id: Mapped[Annotated[int, mapped_column(primary_key=True)]]
    user_id: Mapped[Annotated[int, mapped_column(unique=True)]]

