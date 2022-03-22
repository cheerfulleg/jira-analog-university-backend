-- upgrade --
CREATE TABLE IF NOT EXISTS "project" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(250) NOT NULL,
    "description" TEXT
);;
CREATE TABLE IF NOT EXISTS "teammember" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "role" VARCHAR(100),
    "project_id" INT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);-- downgrade --
DROP TABLE IF EXISTS "project";
DROP TABLE IF EXISTS "teammember";
