import json
from schemas import (
    AppointmentCreate,
    RescheduleRequest,
    ChatRequest
)
from agent import extract_intent
from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, Appointment, UserPreference
from schemas import AppointmentCreate
from pydantic import BaseModel

class PreferenceRequest(BaseModel):
    user_id: str
    language: str
    preferred_doctor: str

Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/book")
def book_appointment(data: AppointmentCreate):

    db = SessionLocal()

    existing = db.query(Appointment).filter(
        Appointment.doctor_name == data.doctor_name,
        Appointment.date == data.date,
        Appointment.time == data.time,
        Appointment.status == "booked"
    ).first()

    if existing:
        db.close()

        return {
            "message": "Slot unavailable",
            "alternatives": [
                "11:00 AM",
                "02:00 PM",
                "04:00 PM"
            ]
        }

    appointment = Appointment(
        patient_name=data.patient_name,
        doctor_name=data.doctor_name,
        date=data.date,
        time=data.time,
        status="booked"
    )

    db.add(appointment)

    db.commit()

    db.refresh(appointment)

    db.close()

    return {
        "message": "Appointment booked successfully",
        "appointment_id": appointment.id
    }
@app.get("/appointments")
def get_appointments():

    db = SessionLocal()

    appointments = db.query(Appointment).all()

    db.close()

    return appointments
@app.put("/cancel/{appointment_id}")
def cancel_appointment(appointment_id: int):

    db = SessionLocal()

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        db.close()
        return {"message": "Appointment not found"}

    appointment.status = "cancelled"

    db.commit()

    db.close()

    return {
        "message": "Appointment cancelled successfully"
    }
@app.put("/reschedule/{appointment_id}")
def reschedule_appointment(
    appointment_id: int,
    data: RescheduleRequest
):

    db = SessionLocal()

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        db.close()
        return {"message": "Appointment not found"}

    existing = db.query(Appointment).filter(
        Appointment.doctor_name == appointment.doctor_name,
        Appointment.date == data.date,
        Appointment.time == data.time,
        Appointment.status == "booked"
    ).first()

    if existing:
        db.close()
        return {
            "message": "Requested slot unavailable"
        }

    appointment.date = data.date
    appointment.time = data.time
    appointment.status = "rescheduled"

    db.commit()

    db.close()

    return {
        "message": "Appointment rescheduled successfully"
    }

@app.post("/intent")
def detect_intent(data: ChatRequest):

    result = extract_intent(data.message)

    cleaned = result.replace("```json", "").replace("```", "").strip()

    parsed = json.loads(cleaned)

    return parsed

@app.post("/ai-book")
def ai_book(data: ChatRequest):

    result = extract_intent(data.message)

    if isinstance(result, str):
        cleaned = result.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(cleaned)
    else:
        parsed = result

    if parsed.get("intent") != "book":
        return {
            "message": "Intent is not booking"
        }

    db = SessionLocal()

    appointment = Appointment(
        patient_name="AI User",
        doctor_name=parsed["doctor"],
        date=parsed["date"],
        time=parsed["time"],
        status="booked"
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    db.close()
    
    return {
        "message": "Appointment booked successfully",
        "appointment_id": appointment.id
    }

@app.post("/preferences")
def save_preferences(data: PreferenceRequest):

    db = SessionLocal()

    pref = UserPreference(
        user_id=data.user_id,
        language=data.language,
        preferred_doctor=data.preferred_doctor
    )

    db.add(pref)

    db.commit()

    db.close()

    return {
        "message": "Preferences saved"
    }

@app.get("/preferences/{user_id}")
def get_preferences(user_id: str):

    db = SessionLocal()

    pref = db.query(UserPreference).filter(
        UserPreference.user_id == user_id
    ).first()

    db.close()

    if not pref:
        return {
            "message": "No preferences found"
        }

    return {
        "user_id": pref.user_id,
        "language": pref.language,
        "preferred_doctor": pref.preferred_doctor
    }