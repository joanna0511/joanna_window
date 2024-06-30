import requests
import json

# 下載 JSON 資料
url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
response = requests.get(url)
data = response.json()

# 格式化並顯示下載的 JSON 資料
formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
print(formatted_data)

#ON CONFLICT (updatetime, sna) DO UPDATE SET
