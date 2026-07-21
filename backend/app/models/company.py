from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    email = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="companies")
    website = Column(String, nullable=True)