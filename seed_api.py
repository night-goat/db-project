import requests
import sqlite3
import xml.etree.ElementTree as ET


def update_emergency_data():
    conn = sqlite3.connect("db/emergency.db")
    cur = conn.cursor()

    BASE_URL = "http://apis.data.go.kr/B552657/ErmctInfoInqireService"
    SERVICE_KEY = "54a210e62143f356fa795088187d6e979f466fb935ce200d83ee264183b0e084"

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

    def to_int(v, default=0):
        try:
            return int(v)
        except:
            return default

    for stage1, stage2_list in region.items():
        for stage2 in stage2_list:

            

            # ==========================
            # 병원 기본 정보 + 주소 
            # ==========================
            info_params = {
                "serviceKey": SERVICE_KEY,
                "Q0": stage1,
                "Q1": stage2,
                "pageNo": 1,
                "numOfRows": 100
            }

            res = requests.get(
                f"{BASE_URL}/getEgytListInfoInqire",
                params=info_params
            )

            root = ET.fromstring(res.text)
            items = root.findall(".//item")

            for item in items:
                hpid = item.findtext("hpid")
                dutyname = item.findtext("dutyName")
                dutyaddr = item.findtext("dutyAddr")
                dutytel3 = item.findtext("dutyTel3")

                cur.execute("""
                    INSERT OR REPLACE INTO HOSPITAL
                    (hpid, dutyname, stage1, stage2, dutytel3, dutyaddr)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (hpid, dutyname, stage1, stage2, dutytel3, dutyaddr))

            # ==========================
            #병상 실시간 정보 (STAGE1, STAGE2)
            # ==========================
            bed_params = {
                "serviceKey": SERVICE_KEY,
                "STAGE1": stage1,
                "STAGE2": stage2,
                "pageNo": 1,
                "numOfRows": 100
            }

            res = requests.get(
                f"{BASE_URL}/getEmrrmRltmUsefulSckbdInfoInqire",
                params=bed_params
            )

            root = ET.fromstring(res.text)
            items = root.findall(".//item")

            for item in items:
                hpid = item.findtext("hpid")

                hvec = to_int(item.findtext("hvec"))
                hvgc = to_int(item.findtext("hvgc"))
                hvncc = to_int(item.findtext("hvncc"))
                hvicc = to_int(item.findtext("hvicc"))
                hvidate = item.findtext("hvidate")

                cur.execute("""
                    INSERT OR REPLACE INTO BedStatus
                    (hpid, hvec, hvgc, hvncc, hvicc, hvidate)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (hpid, hvec, hvgc, hvncc, hvicc, hvidate))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    update_emergency_data()