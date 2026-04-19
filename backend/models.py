from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from db import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

class Route(Base):
    __tablename__ = "route"

    route_id = Column(Integer, primary_key=True, index=True)
    src_latitude = Column(DECIMAL)
    src_longitude = Column(DECIMAL)
    src_address = Column(String)
    dest_latitude = Column(DECIMAL)
    dest_longitude = Column(DECIMAL)
    dest_address = Column(String)
    distance_km = Column(DECIMAL)
    estimated_duration_minutes = Column(Integer)


class Platform(Base):
    __tablename__ = "platform"

    platform_id = Column(Integer, primary_key=True, index=True)
    platform_name = Column(String)
    base_fare = Column(DECIMAL)
    per_km_rate = Column(DECIMAL)
    surge_multiplier = Column(DECIMAL)
    avg_rating = Column(DECIMAL)
    typical_wait_time = Column(Integer)


class FarePrediction(Base):
    __tablename__ = "fare_prediction"

    prediction_id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("route.route_id"))
    platform_id = Column(Integer, ForeignKey("platform.platform_id"))
    predicted_fare = Column(DECIMAL)
    surge_applied = Column(DECIMAL)
    ride_type = Column(String)
    prediction_timestamp = Column(TIMESTAMP, default=func.now())
