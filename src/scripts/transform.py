import os
import json

def load_data(directory="temp_data"):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                try:
                    content = json.load(file)
                    if isinstance(content, dict):
                        data.append(content)
                except json.JSONDecodeError:
                    print(f"Lỗi khi đọc {filename}, bỏ qua.")
    return data

def clean_data(raw_data):
    cleaned = []
    for entry in raw_data:
        cleaned_entry = {
            "location": entry.get("location", {}).get("name", "Unknown"),
            "temperature": entry.get("current", {}).get("temp_c"),
            "humidity": entry.get("current", {}).get("humidity"),
            "wind_kph": entry.get("current", {}).get("wind_kph"),
            "traffic_speed": entry.get("flowSegmentData", {}).get("currentSpeed"),
            "traffic_free_flow_speed": entry.get("flowSegmentData", {}).get("freeFlowSpeed")
        }
        if cleaned_entry["temperature"] is not None and cleaned_entry["humidity"] is not None:
            cleaned.append(cleaned_entry)
    return cleaned

def save_cleaned_data(cleaned_data, output_file="cleaned_data.json"):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(cleaned_data, file, indent=4, ensure_ascii=False)
    print(f"Dữ liệu đã được làm sạch và lưu vào {output_file}")

if __name__ == "__main__":
    raw_data = load_data()
    cleaned_data = clean_data(raw_data)
    save_cleaned_data(cleaned_data)