PRAGMA FOREIGN_KEYS = on;

CREATE TABLE Mod (
	"id" INTEGER UNIQUE DEFAULT 0,

	"name" VARCHAR(255) UNIQUE NOT NULL,
	"version" VARCHAR(15) DEFAULT '1.0.0.0',
	"active" BOOLEAN DEFAULT 0,
	"index" INTEGER UNIQUE DEFAULT 0,

	CHECK ("id" > -1 AND "index" > -1),

	PRIMARY KEY ("id")
);

CREATE TABLE Plugin (
	"mod" INTEGER DEFAULT 0,
	"name" VARCHAR(255) DEFAULT 'undefined',

	"active" BOOLEAN DEFAULT 0,
	"index" INTEGER UNIQUE DEFAULT 0,

	CHECK ("index" > -1 AND "index" < 256),

	FOREIGN KEY ("mod") REFERENCES Mod ("id") ON DELETE CASCADE,
	PRIMARY KEY ("mod", "name")
);

CREATE VIEW Installers AS
	SELECT "name", "version", "active", "index"
	FROM Mod
	ORDER BY "index" ASC;

CREATE VIEW InstalledMods AS
	SELECT "name"
	FROM Mod
	WHERE Mod."active" = 1
	ORDER BY "index" ASC;

CREATE VIEW Plugins AS
	SELECT Plugin."name", Plugin."index", Plugin."mod"
	FROM Plugin
	INNER JOIN Mod ON Plugin."mod" = Mod."id"
	WHERE Mod."active" = 1
	ORDER BY Plugin."index" ASC;

CREATE VIEW InstalledPlugins AS
	SELECT Plugin."name"
	FROM Plugin
	INNER JOIN Mod ON Plugin."mod" = Mod."id"
	WHERE Mod."active" = 1 AND Plugin."active" = 1
	ORDER BY Plugin."index" ASC;


CREATE UNIQUE INDEX ind_mod_name ON Mod("name");
