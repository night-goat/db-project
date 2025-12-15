import requests
import sqlite3
from datetime import datetime
import xml.etree.ElementTree as ET

# ------------------------------
# DB 연결
# ------------------------------
conn = sqlite3.connect("emergency.db")
cursor = conn.cursor()

# ------------------------------
# OpenAPI 요청
# ------------------------------
url = "http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEmrrmRltmUsefulSckbdInfoInqire"

params = {
    "serviceKey": "54a210e62143f356fa795088187d6e979f466fb935ce200d83ee264183b0e084",
    "STAGE1": "서울특별시",
    "STAGE2": "강남구",
    "pageNo": 1,
    "numOfRows": 100
}

res = requests.get(url, params=params)

# ------------------------------
# XML 파싱
# ------------------------------
root = ET.fromstring(res.text)
items = root.findall(".//item")

# ------------------------------
# int 변환 함수
# ------------------------------
def to_int(v, default=0):
    if v is None:
        return default
    s = str(v).strip()
    if s == "":
        return default
    try:
        return int(s)
    except:
        return default

# ------------------------------
# DB 저장
# ------------------------------
for item in items:
    hpid = item.findtext("hpid")
    dutyname = item.findtext("dutyName")
    dutytel3 = item.findtext("dutyTel3")

    hvec = to_int(item.findtext("hvec"))
    hvcc = to_int(item.findtext("hvcc"))
    hvncc = to_int(item.findtext("hvncc"))
    hvccc = to_int(item.findtext("hvccc"))
    hvicc = to_int(item.findtext("hvicc"))

    # 병원 기본 정보
    cursor.execute(
        """
        INSERT OR IGNORE INTO HOSPITAL
        (hpid, dutyname, stage1, stage2, dutytel3)
        VALUES (?, ?, ?, ?, ?)
        """,
        (hpid, dutyname, params["STAGE1"], params["STAGE2"], dutytel3)
    )

    # 응급실 병상 정보
    cursor.execute(
        """
        INSERT INTO BedStatus
        (hpid, hvec, hvidate)
        VALUES (?, ?, ?)
        """,
        (hpid, hvec, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    # 중증질환 병상 정보
    cursor.execute(
        """
        INSERT OR REPLACE INTO SevereCare
        (hpid, hvcc, hvncc, hvccc, hvicc)
        VALUES (?, ?, ?, ?, ?)
        """,
        (hpid, hvcc, hvncc, hvccc, hvicc)
    )

# ------------------------------
# 종료
# ------------------------------
conn.commit()
conn.close()