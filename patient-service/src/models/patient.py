from sqlalchemy import Column, Integer, String, Date
from src.config.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    birth_date = Column(Date)
    health_conditions = Column(String)
    gender = Column(String)
    address = Column(String)
