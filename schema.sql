CREATE TABLE HOSPITAL(
    hpid TEXT NOT NULL,
    dutyname TEXT NOT NULL,
    stage1 TEXT NOT NULL,
    stage2 TEXT NOT NULL,
    dutytel3 TEXT,
    PRIMARY KEY (hpid)
);

CREATE TABLE BedStatus (
    hpid TEXT PRIMARY KEY,
    hvec INTEGER,   -- 응급실 병상
    hvgc INTEGER,   -- 일반 입원실
    hvncc INTEGER,  -- 신생아 중환자실
    hvicc INTEGER,  -- 일반 중환자실
    hvidate TEXT,
    FOREIGN KEY (hpid) REFERENCES HOSPITAL(hpid)
);

