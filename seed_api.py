import requests
import sqlite3
import xml.etree.ElementTree as ET


def update_emergency_data():
    # ==============================
    # DB 연결
    # ==============================
    conn = sqlite3.connect("db/emergency.db")
    cur = conn.cursor()

    # ==============================
    # API 정보
    # ==============================
    URL = "http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEmrrmRltmUsefulSckbdInfoInqire"
    SERVICE_KEY = "54a210e62143f356fa795088187d6e979f466fb935ce200d83ee264183b0e084"

    # ==============================
    # 지역 설정 (과제용 최소 지역)
    # ==============================
    region = {
        "서울특별시": ["강남구", "용산구", "성동구", "서초구", "종로구"],
        "인천광역시": ["부평구", "연수구", "계양구"],
        "경기도": ["부천시", "광명시", "김포시"],
        "충청북도": ["충주시"],
        "충청남도": ["논산시"],
        "세종특별자치시": ["세종시"],
        "전라남도": ["목포시"],
        "경상남도": ["김해시"]
    }

    # ==============================
    # 안전한 int 변환 함수
    # ==============================
    def to_int(value, default=0):
        try:
            return int(value)
        except:
            return default

    # ==============================
    # 지역별 API 호출
    # ==============================
    for stage1, stage2_list in region.items():
        for stage2 in stage2_list:

            params = {
                "serviceKey": SERVICE_KEY,
                "STAGE1": stage1,
                "STAGE2": stage2,
                "pageNo": 1,
                "numOfRows": 100
            }

            response = requests.get(URL, params=params)
            root = ET.fromstring(response.text)
            items = root.findall(".//item")

            for item in items:
                # --------------------------
                # 기본 병원 정보
                # --------------------------
                hpid = item.findtext("hpid")
                dutyname = item.findtext("dutyName")
                dutytel3 = item.findtext("dutyTel3")

                # --------------------------
                # 병상 / 수용 정보 (최신)
                # --------------------------
                hvec = to_int(item.findtext("hvec"))     # 응급실 병상
                hvgc = to_int(item.findtext("hvgc"))     # 일반 입원실
                hvncc = to_int(item.findtext("hvncc"))   # 신생아 중환자실
                hvicc = to_int(item.findtext("hvicc"))   # 일반 중환자실
                hvidate = item.findtext("hvidate")

                # --------------------------
                # HOSPITAL 테이블 (병원 기본 정보)
                # --------------------------
                cur.execute("""
                    INSERT OR REPLACE INTO HOSPITAL
                    (hpid, dutyname, stage1, stage2, dutytel3)
                    VALUES (?, ?, ?, ?, ?)
                """, (hpid, dutyname, stage1, stage2, dutytel3))

                # --------------------------
                # BedStatus 테이블 (병원당 1행)
                # --------------------------
                cur.execute("""
                    INSERT OR REPLACE INTO BedStatus
                    (hpid, hvec, hvgc, hvncc, hvicc, hvidate)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (hpid, hvec, hvgc, hvncc, hvicc, hvidate))

    # ==============================
    # 마무리
    # ==============================
    conn.commit()
    conn.close()


# 직접 실행 시에도 동작하도록
if __name__ == "__main__":
    update_emergency_data()