from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base, str_256


class AccountsData(Base):
    __tablename__ = "accounts"

    """ Variables
    
    :param user_id: primary key
    :param service: the user's selected service
    :param date_client: the user's selected date
    """

    user_id: Mapped[
        Annotated[int, mapped_column(unique=True, primary_key=True, nullable=False)]
    ]
    service: Mapped[str_256]
    name: Mapped[str_256]
    surname: Mapped[str_256]
    phone: Mapped[str_256]
    date_client: Mapped[str_256]
