import json

if __name__ == "__main__":
    path = r"../res/raw_data.json"
    with open(path, "r", encoding="utf-8") as json_file:
        raw_data = json.load(json_file)
        print(f"length of raw_data: {len(raw_data)}")

    path = r"../res/processed_data.json"
    with open(path, "r", encoding="utf-8") as json_file:
        raw_data = json.load(json_file)
        print(f"length of processed_data: {len(raw_data)}")
