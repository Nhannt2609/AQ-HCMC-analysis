import requests
import json
import os
import time
from unidecode import unidecode
import shutil
from datetime import datetime, timezone
from dotenv import load_dotenv

def extract_data():
    load_dotenv()
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    TRAFFIC_API_KEY = os.getenv("TRAFFIC_API_KEY")
    
    states_list = ['Ho Chi Minh City', 'Da Nang', 'Hanoi', 'Tinh Binh Duong', 'Tinh Dong Nai', 'Thanh Pho Hai Phong', 'Tinh Ha Tinh', 'Tinh Ba Ria-Vung Tau']
    
    city_state_list = []
    
    if os.path.exists("temp_data"):
        shutil.rmtree("temp_data")
    os.makedirs("temp_data")
    
    for state_info in states_list:
        CITY_URL = f"http://api.airvisual.com/v2/cities?key={WEATHER_API_KEY}&state={state_info}&country=Vietnam"
        city_list = requests.get(CITY_URL).json()
        time.sleep(15)
        if city_list['status'] != 'success':
            continue
        for city in city_list['data']:
            city_state_list.append({"city": city['city'], "state": state_info})
    
    print("🌟 Extract city list completely")
    
    for district in city_state_list:
        Q1 = district["city"]
        Q2 = district["state"]
        WEATHER_URL = f"http://api.airvisual.com/v2/city?city={Q1}&state={Q2}&country=Vietnam&key={WEATHER_API_KEY}"
        
        weather_data = requests.get(WEATHER_URL).json()
        if weather_data['status'] != 'success': 
            continue
        now_utc = datetime.now(timezone.utc)
        print("🗾 District:", Q1, " - State:", Q2)
        print("⌚ Time now:", now_utc)
        print("⌛ Time API weather:", weather_data["data"]["current"]["weather"]["ts"])
        print("⌛ Time API pollution:", weather_data["data"]["current"]["pollution"]["ts"])
        
        # Kiểm tra thời gian cập nhật có trùng với lần trước không
        weather_ts = datetime.strptime(weather_data["data"]["current"]["weather"]["ts"], "%Y-%m-%dT%H:%M:%S.%fZ").hour
        pollution_ts = datetime.strptime(weather_data["data"]["current"]["pollution"]["ts"], "%Y-%m-%dT%H:%M:%S.%fZ").hour
        
        # if now_utc.hour != weather_ts and now_utc.hour != pollution_ts:
        #     print("⏳ No new data for this district, skipping...")
        #     continue

        coordinates = weather_data["data"]["location"]["coordinates"]
        lat, lon = coordinates[1], coordinates[0]
        TRAFFIC_URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={TRAFFIC_API_KEY}"
        traffic_data = requests.get(TRAFFIC_URL).json()
        if "error" in traffic_data:
            continue

        time.sleep(15)
        
        city_filename = unidecode(district["city"]).replace(" ", "_")
        with open(f"temp_data/weather_{city_filename}.json", "w") as wf:
            json.dump(weather_data, wf, indent=4)
        with open(f"temp_data/traffic_{city_filename}.json", "w") as tf:
            json.dump(traffic_data, tf, indent=4)
        
        
        print(f"✅ Saved data for {district['city']}, {district['state']}")


if __name__ == "__main__":
    extract_data()