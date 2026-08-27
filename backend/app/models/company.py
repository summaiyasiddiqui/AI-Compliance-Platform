from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)

    company_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    email = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"), index=True)

    owner = relationship("User", back_populates="companies")
    website = Column(String, nullable=True)

    __table_args__ = (
        Index("ix_companies_owner_id_company_name", "owner_id", "company_name"),
    )