from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from src.core.database import get_db
from src.core.models import Driver

app = FastAPI(title="Uber for Dogs API", version="0.1.0")

class RideRequest(BaseModel):
    dog_name: str
    breed: str
    pickup_lon: float
    pickup_lat: float

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected ({e})"
    return {"status": "sniffing_around", "service": "online", "database": db_status}

@app.post("/api/v1/rides/request")
def request_ride(payload: RideRequest, db: Session = Depends(get_db)):
    # 1. Construct a spatial geometry point from the incoming coordinates
    pickup_point = func.ST_SetSRID(func.ST_MakePoint(payload.pickup_lon, payload.pickup_lat), 4326)

    # 2. Query the database for the nearest online driver
    # ST_DistanceSphere calculates accurate great-circle distance in meters
    result = db.query(
        Driver,
        func.ST_DistanceSphere(Driver.current_location, pickup_point).label("distance_meters")
    ).filter(Driver.is_online == True) \
     .order_by(func.ST_DistanceSphere(Driver.current_location, pickup_point)) \
     .first()

    if not result:
        raise HTTPException(status_code=404, detail="No available drivers nearby.")

    # 3. Extract the tuple result and convert math for the user
    driver, distance_meters = result
    distance_miles = round(distance_meters * 0.000621371, 2)
    
    # Rough ETA calculation assuming standard city speeds (approx 20mph)
    eta_minutes = max(1, int(distance_miles * 3))

    return {
        "message": "Driver matched successfully!",
        "dispatch_details": {
            "driver_name": driver.dog_name,
            "driver_rating": float(driver.rating),
            "distance_miles": distance_miles,
            "eta_minutes": eta_minutes
        }
    }