from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.core.database import get_db

app = FastAPI(title="Uber for Dogs API", version="0.1.0")

class RideRequest(BaseModel):
    dog_name: str
    breed: str
    pickup_lon: float
    pickup_lat: float

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    # Attempt to run a simple query to verify the connection
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected ({e})"
        
    return {"status": "sniffing_around", "service": "online", "database": db_status}

@app.post("/api/v1/rides/request")
def request_ride(payload: RideRequest):
    return {"message": f"Looking for available drivers near {payload.pickup_lon}, {payload.pickup_lat} for {payload.dog_name}..."}