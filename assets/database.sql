CREATE TABLE Mods (
	"name" VARCHAR(255) UNIQUE NOT NULL,
	"version" VARCHAR(15) DEFAULT 'undef',
	"active" BOOLEAN DEFAULT 0,
	"index" INTEGER DEFAULT 0,

	CHECK ("index" > -1),

	PRIMARY KEY ("name")
);

CREATE TABLE Plugins (
	"name" VARCHAR(255) UNIQUE NOT NULL,
	"active" BOOLEAN DEFAULT 0,
	"index" INTEGER DEFAULT 0,

	CHECK ("index" > -1),

	PRIMARY KEY ("name")
);

CREATE TABLE Preferences (
	"key" VARCHAR(15) NOT NULL,
	"value" VARCHAR(511) DEFAULT 'undef',

	PRIMARY KEY("key")
);

INSERT INTO Preferences ("key", "value") VALUES ('guiWidth', '1000');
INSERT INTO Preferences ("key", "value") VALUES ('guiHeight', '600');
INSERT INTO Preferences ("key", "value") VALUES ('pathGame', 'game');
INSERT INTO Preferences ("key", "value") VALUES ('pathMods', 'mods');
