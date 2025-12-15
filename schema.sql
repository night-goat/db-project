-- ==============================
-- 병원 기본 정보
-- ==============================
CREATE TABLE HOSPITAL (
    hpid TEXT PRIMARY KEY,          -- 병원 ID
    dutyname TEXT NOT NULL,         -- 병원명
    dutyaddr TEXT,                 -- 병원 주소
    stage1 TEXT NOT NULL,           -- 시/도
    stage2 TEXT NOT NULL,           -- 시/군/구
    dutytel3 TEXT                  -- 응급실 전화번호
);

-- ==============================
-- 병상 현황
-- ==============================
CREATE TABLE BedStatus (
    hpid TEXT PRIMARY KEY,          -- 병원 ID
    hvec INTEGER,                   -- 응급실
    hvgc INTEGER,                   -- 입원실
    hvncc INTEGER,                  -- 신생아 중환자실
    hvicc INTEGER,                  -- 일반 중환자실
    hvidate TEXT,                   -- 기준 시각 
    FOREIGN KEY (hpid) REFERENCES HOSPITAL(hpid)
);
