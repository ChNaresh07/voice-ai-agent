from sqlalchemy import Column, Integer, String
from database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_name = Column(String)

    doctor_name = Column(String)

    date = Column(String)

    time = Column(String)

    status = Column(String)

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String)

    language = Column(String)

    preferred_doctor = Column(String)