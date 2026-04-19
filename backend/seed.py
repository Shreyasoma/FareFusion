from db import SessionLocal
from models import Platform

db = SessionLocal()

# Clear existing platforms
db.query(Platform).delete()
db.commit()

platforms = [
    Platform(platform_name="Uber Auto", base_fare=30, per_km_rate=10, avg_rating=4.5, typical_wait_time=5),
    Platform(platform_name="Ola Auto", base_fare=25, per_km_rate=11, avg_rating=4.2, typical_wait_time=8),
    Platform(platform_name="Rapido Auto", base_fare=28, per_km_rate=10.5, avg_rating=4.3, typical_wait_time=6),

    Platform(platform_name="Uber Go", base_fare=50, per_km_rate=15, avg_rating=4.6, typical_wait_time=6),
    Platform(platform_name="Ola Mini", base_fare=45, per_km_rate=16, avg_rating=4.4, typical_wait_time=9),
    Platform(platform_name="Rapido Cab", base_fare=48, per_km_rate=15.5, avg_rating=4.3, typical_wait_time=7),

    Platform(platform_name="Rapido Bike", base_fare=20, per_km_rate=7, avg_rating=4.5, typical_wait_time=4),
    Platform(platform_name="Uber Moto", base_fare=22, per_km_rate=7.5, avg_rating=4.6, typical_wait_time=3),
    Platform(platform_name="Ola Bike", base_fare=18, per_km_rate=8, avg_rating=4.2, typical_wait_time=7),
]

db.add_all(platforms)
db.commit()
db.close()

print("✅ Data seeded successfully!")