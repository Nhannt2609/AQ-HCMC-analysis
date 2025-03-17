import psycopg2
import csv
import json
import os
from uuid import UUID
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(
    dbname="defaultdb",
    user="avnadmin",
    password=DB_PASSWORD,
    host=DB_HOST,
    port="14694",
    sslmode="require"
)
cursor = conn.cursor()

def load_data_time():
    with open("./processed_data/time_data.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            timestamp = row[0]
            year = int(row[1])
            month = int(row[2])
            week = int(row[3])
            day = int(row[4])
            hour = int(row[5])
            minute = int(row[6])
            day_of_week = row[7]
            season = row[8]

            cursor.execute("""
                INSERT INTO "dim_time" (timestamp,year,month,week,day,hour,minute,day_of_week,season)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (timestamp) DO NOTHING;
            """, (timestamp,year,month,week,day,hour,minute,day_of_week,season))
            
def load_data_location():
    with open("./districts.json", "r", encoding="utf-8") as file:
        data = json.load(file)

        for row in data:
            lat, lon = row["lat_lon"].split(",")
            cursor.execute("""
                INSERT INTO dim_location (location_id, latitude, longitude, state, country)
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT (location_id) DO NOTHING;
            """, (
                row["district"],
                float(lat),
                float(lon),
                row["state"],
                "Vietnam"
            ))
            
def load_data_traffic():        
    with open("./processed_data/traffic_data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute("""
                INSERT INTO dim_traffic (
                    traffic_id, frc, current_speed, free_flow_speed, congestion_level,
                    current_travel_time, free_flow_travel_time, confidence, delay_time,
                    congestion_index, traffic_efficiency, data_reliability, adjusted_congestion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (traffic_id) DO NOTHING
            """, (
                str(UUID(row["traffic_id"])),
                row["frc"],
                float(row["current_speed"]),
                float(row["free_flow_speed"]),
                float(row["congestion_level"]),
                float(row["current_travel_time"]),
                float(row["free_flow_travel_time"]),
                float(row["confidence"]),
                float(row["delay_time"]),
                float(row["congestion_index"]),
                float(row["traffic_efficiency"]),
                row["data_reliability"],
                float(row["adjusted_congestion"])
            ))
            
def load_data_weather():
    with open("./processed_data/weather_data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
            INSERT INTO dim_weather (
                weather_id, temperature, pressure, humidity, wind_speed,
                wind_direction, feels_like_temp, heat_index, weather_condition
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (weather_id) DO NOTHING
        """, (
            str(UUID(row["weather_id"])),
            float(row["temperature"]),
            float(row["pressure"]),
            float(row["humidity"]),
            float(row["wind_speed"]),
            float(row["wind_direction"]),
            float(row["feels_like_temp"]),
            float(row["heat_index"]),
            row["weather_condition"]
        ))
            
def load_data_aqi():
    with open("./processed_data/fact_data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            fact_id = str(UUID(row["fact_id"]))
            traffic_id = str(UUID(row["traffic_id"]))
            weather_id = str(UUID(row["weather_id"]))

            cursor.execute("""
                INSERT INTO fact_aqi (
                    fact_id, aqi_us, main_us, aqi_cn, main_cn, timestamp,
                    aqi_us_category, aqi_cn_category, aqi_avg, main_pollutant,
                    severe_pollution, traffic_id, weather_id, location_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (fact_id) DO NOTHING
            """, (
                fact_id,
                int(row["aqi_us"]),
                row["main_us"],
                int(row["aqi_cn"]),
                row["main_cn"],
                row["timestamp"],
                row["aqi_us_category"],
                row["aqi_cn_category"],
                float(row["aqi_avg"]),
                row["main_pollutant"],
                row["severe_pollution"],
                traffic_id,
                weather_id,
                row["location_id"]
            ))

def load_data():
       
    load_data_time()
    load_data_location()
    load_data_traffic()
    load_data_weather()
    load_data_aqi()

    print("Load hoàn tất ❤️")
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_data()