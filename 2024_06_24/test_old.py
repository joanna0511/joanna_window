import requests
import psycopg2
import json
from datetime import datetime

# 下載 JSON 資料
url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
response = requests.get(url)
data = response.json()

# 嘗試連接 PostgreSQL 資料庫
try:
    conn = psycopg2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    cursor = conn.cursor()
except psycopg2.OperationalError as e:
    print("Unable to connect to the database")
    print(e)
    exit()

# 建立 youbike2 資料表，如果尚未建立
create_table_query = '''
CREATE TABLE IF NOT EXISTS youbike2 (
    _id SERIAL PRIMARY KEY,
    sna VARCHAR(50) NOT NULL,
    sarea VARCHAR(50),
    ar VARCHAR(100),
    mday TIMESTAMP,
    updatetime TIMESTAMP,
    total SMALLINT,
    rent_bikes SMALLINT,
    return_bikes SMALLINT,
    lat REAL,
    lng REAL,
    act BOOLEAN,
    UNIQUE (updatetime, sna)
);
'''
cursor.execute(create_table_query)
conn.commit()

# 資料清理函數
def clean_data(item):
    def safe_get(key, default=None):
        return item.get(key) if item.get(key) is not None else default

    # 清理數字型資料
    def clean_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def clean_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    # 解析 mday 欄位，假設格式為 '%Y-%m-%d %H:%M:%S'
    mday_str = safe_get("mday", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        mday = datetime.strptime(mday_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        mday = datetime.now()

    return {
        "sna": safe_get("sna", ""),
        "sarea": safe_get("sarea", ""),
        "ar": safe_get("ar", ""),
        "mday": mday,
        "updatetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total": clean_int(safe_get("tot", 0)),
        "rent_bikes": clean_int(safe_get("sbi", 0)),
        "return_bikes": clean_int(safe_get("bemp", 0)),
        "lat": clean_float(safe_get("lat", 0.0)),
        "lng": clean_float(safe_get("lng", 0.0)),
        "act": safe_get("act", 0) == 1  # 將 act 轉換為布林值
    }

# 插入資料到 youbike2 資料表
insert_query = '''
INSERT INTO youbike2 (sna, sarea, ar, mday, updatetime, total, rent_bikes, return_bikes, lat, lng, act)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (updatetime, sna) DO UPDATE SET
sarea = EXCLUDED.sarea,
ar = EXCLUDED.ar,
mday = EXCLUDED.mday,
total = EXCLUDED.total,
rent_bikes = EXCLUDED.rent_bikes,
return_bikes = EXCLUDED.return_bikes,
lat = EXCLUDED.lat,
lng = EXCLUDED.lng,
act = EXCLUDED.act;
'''

for item in data:
    cleaned_item = clean_data(item)
    # 調試輸出清理後的數據 - 新增部分
    print(cleaned_item)  # <<<<<< 新增：輸出清理後的數據以便調試
    cursor.execute(insert_query, (
        cleaned_item["sna"],
        cleaned_item["sarea"],
        cleaned_item["ar"],
        cleaned_item["mday"],
        cleaned_item["updatetime"],
        cleaned_item["total"],
        cleaned_item["rent_bikes"],
        cleaned_item["return_bikes"],
        cleaned_item["lat"],
        cleaned_item["lng"],
        cleaned_item["act"]
    ))

# 提交變更並關閉連接
conn.commit()
cursor.close()
conn.close()
