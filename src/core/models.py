from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from src.core.database import Base

class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Dog(Base):
    __tablename__ = "dogs"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"))
    name = Column(String(50), nullable=False)
    breed = Column(String(50))
    size = Column(String(20))
    chasing_squirrels_probability = Column(Integer, default=100)

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    dog_name = Column(String(50), nullable=False)
    rating = Column(Numeric(3, 2), default=5.00)
    is_online = Column(Boolean, default=False)
    # SRID 4326 enforces standard WGS 84 longitude/latitude coordinates
    current_location = Column(Geometry(geometry_type='POINT', srid=4326))

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    dog_name = Column(String(50), nullable=False)
    pickup_lon = Column(Numeric(9, 6))
    pickup_lat = Column(Numeric(9, 6))
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    status = Column(String(20), default="requested") # requested, accepted, in_progress, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())