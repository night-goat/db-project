import requests
import sqlite3
from datetime import datetime

#파일, 커서 생성
conn = sqlite3.connect("emergency.db")
cursor = conn.cursor()

#------------------------------
#openapi 데이터 요청
#------------------------------


url = "http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEmrrmRltmUsefulSckbdInfoInqire"
params = {
    "serviceKey": "54a210e62143f356fa795088187d6e979f466fb935ce200d83ee264183b0e084",
    "STAGE1": "서울특별시",
    "STAGE2": "강남구",
    "pageNo": 1,
    "numOfRows": 100,
    "resultType": "json"
}

res = requests.get(url, params=params)
data = res.json()
items = data['response']['body']['items']['item']

#------------------------------
#int 변환 함수
#------------------------------

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

#------------------------------
#DB에 데이터 저장
#------------------------------


for item in items:
    cursor.execute(
        """
        INSERT OR IGNORE INTO HOSPITAL
        (hpid, dutyname, stage1, stage2, dutytel3)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            item.get("hpid"),
            item.get("dutyName"),
            params["STAGE1"],
            params["STAGE2"],
            item.get("dutyTel3")
        )
    )

    cursor.execute(
        """
        INSERT INTO BedStatus
        (hpid, hvec, hvidate)
        VALUES (?, ?, ?)
        """,
        (
            item.get("hpid"),
            to_int(item.get("hvec")),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    cursor.execute(
        """
        INSERT OR REPLACE INTO SevereCare
        (hpid, hvcc, hvncc, hvccc, hvicc)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            item.get("hpid"),
            to_int(item.get("hvcc")),
            to_int(item.get("hvncc")),
            to_int(item.get("hvccc")),
            to_int(item.get("hvicc"))
        )
    )




conn.commit()
conn.close()