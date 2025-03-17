CREATE TABLE dim_time (
    timestamp TIMESTAMP WITH TIME ZONE PRIMARY KEY,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    week INTEGER NOT NULL,
    day INTEGER NOT NULL,
    hour INTEGER NOT NULL,
    minute INTEGER NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    season VARCHAR(20) NOT NULL
);

CREATE TABLE dim_location (
    location_id VARCHAR(255) PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    state VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL
);

CREATE TABLE dim_traffic (
    traffic_id UUID PRIMARY KEY,
    frc VARCHAR(10) NOT NULL,
    current_speed FLOAT NOT NULL,
    free_flow_speed FLOAT NOT NULL,
    congestion_level FLOAT NOT NULL,
    current_travel_time FLOAT NOT NULL,
    free_flow_travel_time FLOAT NOT NULL,
    confidence FLOAT NOT NULL, 
    delay_time FLOAT NOT NULL,
    congestion_index FLOAT NOT NULL,
    traffic_efficiency FLOAT NOT NULL,
    data_reliability VARCHAR(20) NOT NULL,
    adjusted_congestion FLOAT NOT NULL
);

CREATE TABLE dim_weather (
    weather_id UUID PRIMARY KEY,
    temperature FLOAT NOT NULL,
    pressure FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    wind_speed FLOAT NOT NULL,
    wind_direction FLOAT NOT NULL,
    feels_like_temp FLOAT NOT NULL,
    heat_index FLOAT NOT NULL,
    weather_condition VARCHAR(50) NOT NULL
);

CREATE TABLE fact_aqi (
    fact_id UUID PRIMARY KEY,
    aqi_us INTEGER NOT NULL,
    main_us VARCHAR(50) NOT NULL,
    aqi_cn INTEGER NOT NULL,
    main_cn VARCHAR(50) NOT NULL,
    aqi_us_category VARCHAR(50) NOT NULL,
    aqi_cn_category VARCHAR(50) NOT NULL,
    aqi_avg FLOAT NOT NULL,
    main_pollutant VARCHAR(50) NOT NULL, 
    severe_pollution VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL REFERENCES dim_time(timestamp) ON DELETE RESTRICT ON UPDATE RESTRICT,
    traffic_id UUID NOT NULL REFERENCES dim_traffic(traffic_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    weather_id UUID NOT NULL REFERENCES dim_weather(weather_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    location_id VARCHAR(255) NOT NULL REFERENCES dim_location(location_id) ON DELETE RESTRICT ON UPDATE RESTRICT
);



