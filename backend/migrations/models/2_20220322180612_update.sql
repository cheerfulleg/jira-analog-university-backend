-- upgrade --
CREATE TABLE IF NOT EXISTS "column" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "project_id" INT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "column";
