-- upgrade --
CREATE TABLE IF NOT EXISTS "task" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(150) NOT NULL,
    "description" TEXT,
    "column_id" INT NOT NULL REFERENCES "column" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "task";
