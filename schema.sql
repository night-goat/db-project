CREATE TABLE HOSPITAL(
    hpid TEXT NOT NULL,
    dutyname TEXT NOT NULL,
    stage1 TEXT NOT NULL,
    stage2 TEXT NOT NULL,
    dutytel3 TEXT,
    PRIMARY KEY (hpid)
);

CREATE TABLE BedStatus(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hpid TEXT NOT NULL,
    hvec INTEGER NOT NULL,
    hvidate TEXT NOT NULL,
    FOREIGN KEY (hpid) REFERENCES HOSPITAL(hpid)
);

CREATE TABLE SevereCare(
    hpid TEXT NOT NULL,
    hvcc INTEGER NOT NULL,   -- 신경중환자
    hvncc INTEGER NOT NULL,  -- 신생중환자
    hvccc INTEGER NOT NULL,  -- 흉부중환자
    hvicc INTEGER NOT NULL,  -- 일반중환자
    PRIMARY KEY (hpid),
    FOREIGN KEY (hpid) REFERENCES Hospital(hpid)
);