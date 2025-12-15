from flask import Flask, render_template, request
import sqlite3
from seed_api import update_emergency_data

# 서버 시작 시 데이터 갱신
print("🔄 응급실 데이터 갱신 중...")
update_emergency_data()
print("✅ 응급실 데이터 갱신 완료")

app = Flask(__name__)

DB_PATH = "db/emergency.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("search.html")


@app.route("/search")
def search():
    stage1 = request.args.get("stage1")
    stage2 = request.args.get("stage2")

    conn = get_db()
    cur = conn.cursor()

    # 전체 선택
    if stage2 == "" or stage2 is None:
        cur.execute("""
            SELECT H.dutyname, H.dutytel3,
                   B.hvec, B.hvgc, B.hvncc, B.hvicc, B.hvidate
            FROM HOSPITAL H, BedStatus B
            WHERE H.hpid = B.hpid
              AND H.stage1 = ?
        """, (stage1,))
    else:
        # 특정 구 선택
        cur.execute("""
            SELECT H.dutyname, H.dutytel3,
                   B.hvec, B.hvgc, B.hvncc, B.hvicc, B.hvidate
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


if __name__ == "__main__":
    app.run(debug=True)