import requests
import sqlite3

#파일, 커서 생성
conn = sqlite3.connect("emergency.db")
cursor = conn.cursor()

#------------------------------
#openapi 데이터 요청
#------------------------------


url = "https://apis.data.go.kr/B552657/ErmctInfoInqireService"
params = {
    "serviceKey": "54a210e62143f356fa795088187d6e979f466fb935ce200d83ee264183b0e084",
    "pageNo": 1,
    "numOfRows": 100
}

res = request.get(url, params=params)
data = res.json()

#------------------------------
#DB에 데이터 저장
#------------------------------


conn.commit()
conn.close()