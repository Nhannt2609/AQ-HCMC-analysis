import os
import json
import pandas as pd
import uuid
from datetime import datetime

def categorize_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"
    
def feels_like(temp, wind_speed):
    return 13.12 + 0.6215 * temp - 11.37 * (wind_speed ** 0.16) + 0.3965 * temp * (wind_speed ** 0.16)

def heat_index(temp, humidity):
    return temp + 0.5555 * ((6.112 * 10 ** (7.5 * temp / (237.7 + temp)) * humidity / 100) - 10)

def weather_condition(temp, humidity, wind_speed):
    if temp > 30 and humidity > 70:
        return "Hot and Humid"
    elif temp < 10 and wind_speed > 15:
        return "Cold and Windy"
    elif humidity < 30 and wind_speed > 20:
        return "Dry and Windy"
    else:
        return "Normal"

def transform_data():
    # Đọc danh sách các file JSON trong thư mục temp_data
    weather_files = [f for f in os.listdir("temp_data") if f.startswith("weather_") and f.endswith(".json")]
    traffic_files = [f for f in os.listdir("temp_data") if f.startswith("traffic_") and f.endswith(".json")]

    # Tạo danh sách chứa dữ liệu
    weather_data = []
    traffic_data = []
    aqi_data = []

    # Đọc dữ liệu giao thông
    for file in traffic_files:
        with open(f"temp_data/{file}", "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if "flowSegmentData" in data:  # Kiểm tra JSON hợp lệ
                current_speed = data["flowSegmentData"]["currentSpeed"]
                free_flow_speed = data["flowSegmentData"]["freeFlowSpeed"]
                current_travel_time = data["flowSegmentData"]["currentTravelTime"]
                free_flow_travel_time = data["flowSegmentData"]["freeFlowTravelTime"]
                confidence = data["flowSegmentData"]["confidence"]

                traffic_data.append({
                    "district": file.replace("traffic_", "").replace(".json", "").replace("_", " "),
                    "frc": data["flowSegmentData"]["frc"],
                    "current_speed": current_speed,
                    "free_flow_speed": free_flow_speed,
                    "congestion_level": current_speed / free_flow_speed,
                    "current_travel_time": current_travel_time,
                    "free_flow_travel_time": free_flow_travel_time,
                    "confidence": confidence,

                    # Các field mới
                    "delay_time": current_travel_time - free_flow_travel_time,
                    "congestion_index": 1 - (current_speed / free_flow_speed),
                    "traffic_efficiency": (current_speed / free_flow_speed) * 100,
                    "data_reliability": "Low" if confidence < 0.5 else "High",
                    "adjusted_congestion": (current_travel_time - free_flow_travel_time) / free_flow_travel_time
                })

    # Đọc dữ liệu thời tiết
    for file in weather_files:
        with open(f"temp_data/{file}", "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if data["status"] == "success":
                aqi_us = data["data"]["current"]["pollution"]["aqius"]
                aqi_cn = data["data"]["current"]["pollution"]["aqicn"]
                main_us = "PM2.5" if data["data"]["current"]["pollution"]["mainus"] == "p2" else "PM10"
                main_cn = "PM2.5" if data["data"]["current"]["pollution"]["maincn"] == "p2" else "PM10"
                timestamp = data["data"]["current"]["pollution"]["ts"]

                aqi_data.append({
                    "district": file.replace("weather_", "").replace(".json", "").replace("_", " "),
                    "aqi_us": aqi_us,
                    "main_us": main_us,
                    "aqi_cn": aqi_cn,
                    "main_cn": main_cn,
                    "timestamp": timestamp,

                    "aqi_us_category": categorize_aqi(aqi_us),
                    "aqi_cn_category": categorize_aqi(aqi_cn),
                    "aqi_avg": (aqi_us + aqi_cn) / 2,
                    "main_pollutant": "PM2.5" if "PM2.5" in [main_us, main_cn] else "PM10",
                    "severe_pollution": "Yes" if aqi_us > 150 or aqi_cn > 150 else "No"
                })
                
                temp = data["data"]["current"]["weather"]["tp"]
                pressure = data["data"]["current"]["weather"]["pr"]
                humidity = data["data"]["current"]["weather"]["hu"]
                wind_speed = data["data"]["current"]["weather"]["ws"]
                wind_direction = data["data"]["current"]["weather"]["wd"]
                timestamp = data["data"]["current"]["pollution"]["ts"]
                
                weather_data.append({
                    "district": file.replace("weather_", "").replace(".json", "").replace("_", " "),
                    "timestamp": timestamp,
                    "temperature": temp,
                    "pressure": pressure,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                    "wind_direction": wind_direction,

                    "feels_like_temp": feels_like(temp, wind_speed),
                    "heat_index": heat_index(temp, humidity),
                    "weather_condition": weather_condition(temp, humidity, wind_speed),
                })
            else:
                print(f"Lỗi: Không thể đọc dữ liệu từ {file}, status: {data['status']}")

    # Chuyển dữ liệu thành DataFrame
    df_weather = pd.DataFrame(weather_data)
    df_aqi = pd.DataFrame(aqi_data)
    df_traffic = pd.DataFrame(traffic_data)

    # Chuyển DataFrame thành csv theo star schema đã thiết kế
    # Tạo PK cho các bảng dimension
    df_traffic["traffic_id"] = [uuid.uuid4() for _ in range(len(df_traffic))]
    df_weather["weather_id"] = [uuid.uuid4() for _ in range(len(df_weather))]
    # Merge bảng theo 'district'
    df_aqi_traffic = pd.merge(df_aqi, df_traffic, on="district", how="inner")
    df_fact = pd.merge(df_aqi_traffic, df_weather, on="district", how="inner")
    df_fact["fact_id"] = [uuid.uuid4() for _ in range(len(df_fact))]

    # Xử lý các field trong DataFrame
    df_traffic.drop("district", axis=1, inplace=True)
    df_weather.drop(columns=['district', 'timestamp'], axis=1, inplace=True)

    columns_to_drop = [
        'frc', 'current_speed', 'free_flow_speed', 'congestion_level', 
        'current_travel_time', 'free_flow_travel_time', 'confidence', 
        'delay_time', 'congestion_index', 'traffic_efficiency', 
        'data_reliability', 'adjusted_congestion', 
        'timestamp_y', 'temperature', 'pressure', 'humidity', 
        'wind_speed', 'wind_direction', 'feels_like_temp', 
        'heat_index', 'weather_condition'
    ]
    df_fact.drop(columns=columns_to_drop, axis=1, inplace=True)
    df_fact = df_fact.rename(columns={'timestamp_x' : 'timestamp', 'district': 'location_id'})
    df_fact['timestamp'] = pd.to_datetime(df_fact['timestamp'])

    # Xử lý data time
    df_time = df_fact[['timestamp']].copy()
    df_time = df_time.drop_duplicates() 
    df_time['timestamp'] = pd.to_datetime(df_time['timestamp'])
    # Chuyển đổi timezone sang Asia/Bangkok (UTC+07:00)
    df_time['timestamp'] = df_time['timestamp'].dt.tz_convert('Asia/Bangkok')
    df_time['year'] = df_time['timestamp'].dt.year
    df_time['month'] = df_time['timestamp'].dt.month
    df_time['week'] = df_time['timestamp'].dt.isocalendar().week
    df_time['day'] = df_time['timestamp'].dt.day
    df_time['hour'] = df_time['timestamp'].dt.hour
    df_time['minute'] = df_time['timestamp'].dt.minute
    df_time['day_of_week'] = df_time['timestamp'].dt.day_name()

    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Autumn'

    df_time['season'] = df_time['month'].apply(get_season)

    print(df_fact.columns)

    # Tạo thư mục lưu data đã xử lý
    os.makedirs("processed_data", exist_ok=True)

    # Lưu dữ liệu thành CSV
    df_traffic.to_csv("processed_data/traffic_data.csv", index=False, encoding="utf-8")
    df_weather.to_csv("processed_data/weather_data.csv", index=False, encoding="utf-8")
    df_time.to_csv("processed_data/time_data.csv", index=False, encoding="utf-8")
    df_fact.to_csv("processed_data/fact_data.csv", index=False, encoding="utf-8")

    print("✅ Dữ liệu đã được xử lý và lưu vào processed_data")
    
if __name__ == "__main__":
    transform_data()