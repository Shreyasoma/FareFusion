DROP TABLE IF EXISTS fare_prediction CASCADE;
DROP TABLE IF EXISTS route CASCADE;
DROP TABLE IF EXISTS platform CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);
INSERT INTO users (name, email, password, is_admin)
VALUES ('Admin', 'admin@farefusion.com', 'admin123', TRUE);

CREATE TABLE route (
    route_id SERIAL PRIMARY KEY,
    src_latitude DECIMAL(10,7) NOT NULL,
    src_longitude DECIMAL(10,7) NOT NULL,
    src_address TEXT NOT NULL,
    dest_latitude DECIMAL(10,7) NOT NULL,
    dest_longitude DECIMAL(10,7) NOT NULL,
    dest_address TEXT NOT NULL,
    distance_km DECIMAL(6,2) NOT NULL CHECK (distance_km >= 0),
    estimated_duration_minutes INT CHECK (estimated_duration_minutes >= 0)
);


CREATE TABLE platform (
    platform_id SERIAL PRIMARY KEY,
    platform_name VARCHAR(50) UNIQUE NOT NULL,
    base_fare DECIMAL(6,2) NOT NULL CHECK (base_fare >= 0),
    per_km_rate DECIMAL(6,2) NOT NULL CHECK (per_km_rate >= 0),
    surge_multiplier DECIMAL(3,2) DEFAULT 1.0 CHECK (surge_multiplier >= 1),
    avg_rating DECIMAL(2,1) CHECK (avg_rating BETWEEN 0 AND 5),
    typical_wait_time INT CHECK (typical_wait_time >= 0)
);


CREATE TABLE fare_prediction (
    prediction_id SERIAL PRIMARY KEY,
    route_id INT NOT NULL REFERENCES route(route_id) ON DELETE CASCADE,
    platform_id INT NOT NULL REFERENCES platform(platform_id) ON DELETE CASCADE,
    predicted_fare DECIMAL(7,2) NOT NULL CHECK (predicted_fare >= 0),
    surge_applied DECIMAL(3,2) DEFAULT 1.0 CHECK (surge_applied >= 1),
    ride_type VARCHAR(20) NOT NULL CHECK (ride_type IN ('auto', 'cab', 'bike')),
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_route_id ON fare_prediction(route_id);
CREATE INDEX idx_platform_id ON fare_prediction(platform_id);
CREATE INDEX idx_timestamp ON fare_prediction(prediction_timestamp);

INSERT INTO platform (platform_name, base_fare, per_km_rate, surge_multiplier, avg_rating, typical_wait_time)
VALUES
('Uber Auto', 30, 10, 1.0, 4.5, 5),
('Ola Auto', 25, 11, 1.0, 4.2, 8),
('Rapido Auto', 28, 10.5, 1.0, 4.3, 6),

('Uber Go', 50, 15, 1.0, 4.6, 6),
('Ola Mini', 45, 16, 1.0, 4.4, 9),
('Rapido Cab', 48, 15.5, 1.0, 4.3, 7),

('Rapido Bike', 20, 7, 1.0, 4.5, 4),
('Uber Moto', 22, 7.5, 1.0, 4.6, 3),
('Ola Bike', 18, 8, 1.0, 4.2, 7);

