from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    role = Column(
        String,
        nullable=False,
        default="user"
    )

    companies = relationship(
        "Company",
        back_populates="owner",
        cascade="all, delete"
    )
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True) 