from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("emergency.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    # 일단 버튼만 있는 페이지
    return render_template("index.html")


@app.route("/search")
def search():
    # 🔥 하드코딩 검색 (지금 단계 핵심)
    stage1 = "서울특별시"
    stage2 = "강남구"

    conn = get_db()
    cur = conn.cursor()

    query = """
    SELECT
        H.dutyname,
        H.dutytel3,
        B.hvec,
        S.hvcc,
        S.hvncc,
        S.hvicc
    FROM HOSPITAL H
    JOIN BedStatus B ON H.hpid = B.hpid
    JOIN SevereCare S ON H.hpid = S.hpid
    WHERE H.stage1 = ? AND H.stage2 = ?
    """

    cur.execute(query, (stage1, stage2))
    results = cur.fetchall()
    conn.close()

    return render_template("result.html", hospitals=results)


if __name__ == "__main__":
    app.run(debug=True)