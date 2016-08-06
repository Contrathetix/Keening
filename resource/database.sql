PRAGMA FOREIGN_KEYS = on;

CREATE TABLE Mod (
    name VARCHAR(511) UNIQUE NOT NULL,
    version VARCHAR(15) DEFAULT '1.0.0.0',
    size INTEGER DEFAULT 0,
    files INTEGER DEFAULT 0,
    ind INTEGER DEFAULT 0,

    CHECK (ind > -1),

    PRIMARY KEY (name)
);

CREATE TABLE Data (
    name VARCHAR(31) UNIQUE NOT NULL,
    value VARCHAR(4095) NOT NULL,

    PRIMARY KEY (name)
);

INSERT INTO Data (name, value) VALUES ("pathMods", "D:\ModsMorrowind");
INSERT INTO Data (name, value) VALUES ("pathGame", "D:\ModsMorrowind\Morrowind");
INSERT INTO Data (name, value) VALUES ("pathData", "D:\ModsMorrowind\Morrowind\Data");
INSERT INTO Data (name, value) VALUES ("pathLink", "D:\ModsMorrowind\Keening\SymlinkTree");
INSERT INTO Data (name, value) VALUES ("pathSave", "D:\ModsMorrowind\Morrowind\Saves");
