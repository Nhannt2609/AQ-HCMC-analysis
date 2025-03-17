import requests
import json
import os
import time
from dotenv import load_dotenv

def extract_data():
    load_dotenv()
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    TRAFFIC_API_KEY = os.getenv("TRAFFIC_API_KEY")
    # print(WEATHER_API_KEY)
    # print(TRAFFIC_API_KEY)

    with open("districts.json", "r", encoding="utf-8") as f:
        districts = json.load(f)

    os.makedirs("temp_data", exist_ok=True)
    
    
    for district in districts:
        Q1 = district["name"]
        Q2 = district["state"]
        Q3 = district["lat_lon"]
        WEATHER_URL = f"http://api.airvisual.com/v2/city?city={Q1}&state={Q2}&country=Vietnam&key={WEATHER_API_KEY}"
        TRAFFIC_URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={Q3}&key={TRAFFIC_API_KEY}"
        
        weather_data = requests.get(WEATHER_URL).json()
        traffic_data = requests.get(TRAFFIC_URL).json()
        
        time.sleep(15)
        
        with open(f"temp_data/weather_{district['district'].replace(' ', '_')}.json", "w") as wf:
            json.dump(weather_data, wf, indent=4)
        
        with open(f"temp_data/traffic_{district['district'].replace(' ', '_')}.json", "w") as tf:
            json.dump(traffic_data, tf, indent=4)
        
        print(f"Saved data for {district['district']}")
    
if __name__ == "__main__":
    extract_data()