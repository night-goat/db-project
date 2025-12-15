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
    hvec INTEGER,
    hvidate TEXT,
    FOREIGN KEY (hpid) REFERENCES Hospital(hpid)
);

CREATE TABLE SevereCare (
    hpid TEXT PRIMARY KEY,
    hvcc INTEGER,
    hvncc INTEGER,
    hvicc INTEGER,
    FOREIGN KEY (hpid) REFERENCES Hospital(hpid)
);