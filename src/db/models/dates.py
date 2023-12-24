from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base, str_256


class Dates(Base):
    __tablename__ = "dates"

    """ Variables

    :param user_id: primary key
    :param date_admin: a date that admin wrote
    """

    user_id: Mapped[Annotated[int, mapped_column(primary_key=True)]]
    date_admin: Mapped[str_256]
