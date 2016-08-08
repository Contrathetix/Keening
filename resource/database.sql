PRAGMA FOREIGN_KEYS = on;

CREATE TABLE Mod (
    name VARCHAR(511) UNIQUE NOT NULL,
    version VARCHAR(15) DEFAULT '1.0.0.0',
    ind INTEGER DEFAULT 0,

    CHECK (ind > -1),

    PRIMARY KEY (name)
);
