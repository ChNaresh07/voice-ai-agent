from pydantic import BaseModel

class AppointmentCreate(BaseModel):
    patient_name: str
    doctor_name: str
    date: str
    time: str
from pydantic import BaseModel

class AppointmentCreate(BaseModel):
    patient_name: str
    doctor_name: str
    date: str
    time: str


class RescheduleRequest(BaseModel):
    date: str
    time: str

class ChatRequest(BaseModel):
    message: str