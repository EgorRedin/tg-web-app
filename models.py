from database_init import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger


class User(Base):
    __tablename__ = "users"
    id = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    auto_miner: Mapped[int]
    balance: Mapped[int]
    click_size: Mapped[int]
