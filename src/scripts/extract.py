import requests
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
TRAFFIC_API_KEY = os.getenv("TRAFFIC_API_KEY")
# print(WEATHER_API_KEY)
# print(TRAFFIC_API_KEY)

districts = [
    {"district": "TP Thu Duc – Quan 2", "name": "Binh Thanh", "lat_lon": "10.7731,106.7544"},
    {"district": "Quan 6", "name": "Cho Lon", "lat_lon": "10.75,106.65"},
    {"district": "Quan 7", "name": "Tan Thuan Dong", "lat_lon": "10.75,106.7325"},
    {"district": "Quan 8", "name": "Ho Chi Minh", "lat_lon": "10.75,106.6667"},
    {"district": "TP Thu Duc – Quan 9", "name": "Long Thanh My", "lat_lon": "10.8333,106.8167"},
    {"district": "Quan 12", "name": "Dong Hung Thuan", "lat_lon": "10.8414,106.6208"},
    {"district": "TP Thu Duc – Thu Duc", "name": "Thu Duc", "lat_lon": "10.85,106.75"},
    {"district": "Tan Binh", "name": "Tan Binh", "lat_lon": "10.8025,106.66"},
    {"district": "Binh Tan", "name": "Binh Hung Hoa", "lat_lon": "10.7964,106.6081"},
    {"district": "Binh Thanh", "name": "Gia Dinh", "lat_lon": "10.8,106.7"},
    {"district": "Phu Nhuan", "name": "Phu Nhuan", "lat_lon": "10.7956,106.6739"},
    {"district": "Tan Phu", "name": "Phu Tho Hoa", "lat_lon": "10.7667,106.6333"},
    {"district": "Go Vap", "name": "Go Vap", "lat_lon": "10.8167,106.6833"},
    {"district": "Binh Chanh", "name": "Vinh Loc", "lat_lon": "10.8167,106.5667"},
    {"district": "Hoc Mon", "name": "Hoc Mon", "lat_lon": "10.8894,106.5922"},
    {"district": "Nha Be", "name": "Nha Be", "lat_lon": "10.6833,106.7667"},
    {"district": "Cu Chi", "name": "Cu Chi", "lat_lon": "10.9667,106.4667"},
]

os.makedirs("temp_data", exist_ok=True)

# WEATHER_URL = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={Q}&aqi=yes"
# TRAFFIC_URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={Q}&key={TRAFFIC_API_KEY}"


def extract_data():
    for district in districts:
        Q1 = district["name"]
        Q2 = district["lat_lon"]
        WEATHER_URL = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={Q1}&aqi=yes"
        TRAFFIC_URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={Q2}&key={TRAFFIC_API_KEY}"
        
        weather_data = requests.get(WEATHER_URL).json()
        traffic_data = requests.get(TRAFFIC_URL).json()
        
        time.sleep(2)
        
        with open(f"temp_data/weather_{district['district'].replace(' ', '_')}.json", "w") as wf:
            json.dump(weather_data, wf, indent=4)
        
        with open(f"temp_data/traffic_{district['district'].replace(' ', '_')}.json", "w") as tf:
            json.dump(traffic_data, tf, indent=4)
        
        print(f"Saved data for {district['district']}")
    
if __name__ == "__main__":
    extract_data()