from flask import Flask, render_template, request
import sqlite3
from seed_api import update_emergency_data

app = Flask(__name__)

DB_PATH = "db/emergency.db"


# =========================
# DB 연결 함수
# =========================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# 메인 페이지 (검색)
# =========================
@app.route("/")
def index():
    return render_template("search.html")


# =========================
# 지역별 응급실 조회
# =========================
@app.route("/search")
def search():
    stage1 = request.args.get("stage1")
    stage2 = request.args.get("stage2")

    conn = get_db()
    cur = conn.cursor()

    # 시/도 전체 선택
    if stage2 == "" or stage2 is None:
        cur.execute("""
            SELECT H.dutyname,
                   H.dutyaddr,
                   H.dutytel3,
                   B.hvec,
                   B.hvgc,
                   B.hvncc,
                   B.hvicc,
                   B.hvidate
            FROM HOSPITAL H, BedStatus B
            WHERE H.hpid = B.hpid
              AND H.stage1 = ?
        """, (stage1,))
    else:
        # 특정 시/군/구 선택
        cur.execute("""
            SELECT H.dutyname,
                   H.dutyaddr,
                   H.dutytel3,
                   B.hvec,
                   B.hvgc,
                   B.hvncc,
                   B.hvicc,
                   B.hvidate
            FROM HOSPITAL H, BedStatus B
            WHERE H.hpid = B.hpid
              AND H.stage1 = ?
              AND H.stage2 = ?
        """, (stage1, stage2))

    hospitals = cur.fetchall()
    conn.close()

    title_region = stage2 if stage2 else stage1

    return render_template(
        "result.html",
        hospitals=hospitals,
        stage2=title_region
    )


# =========================
# 잔여 병상 TOP 5
# =========================
@app.route("/top5")
def top5():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT H.dutyname,
               H.dutyaddr,
               H.dutytel3,
               B.hvec,
               B.hvidate
        FROM HOSPITAL H, BedStatus B
        WHERE H.hpid = B.hpid
        ORDER BY B.hvec DESC
        LIMIT 5
    """)

    hospitals = cur.fetchall()
    conn.close()

    return render_template("top5.html", hospitals=hospitals)


# =========================
# 지역별 총 응급실 병상 수
# =========================
@app.route("/region_sum")
def region_sum():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT H.stage1,
               SUM(B.hvec) AS total_beds
        FROM HOSPITAL H, BedStatus B
        WHERE H.hpid = B.hpid
        GROUP BY H.stage1
        ORDER BY total_beds DESC
    """)

    regions = cur.fetchall()
    conn.close()

    return render_template("region_sum.html", regions=regions)


# =========================
# 서버 시작
# =========================
if __name__ == "__main__":
    print("🔄 응급실 데이터 갱신 중...")
    update_emergency_data()
    print("✅ 응급실 데이터 갱신 완료")

    app.run(debug=True)