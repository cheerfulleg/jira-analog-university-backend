-- upgrade --
ALTER TABLE "column" RENAME COLUMN "name" TO "title";
ALTER TABLE "task" RENAME COLUMN "name" TO "title";
-- downgrade --
ALTER TABLE "task" RENAME COLUMN "title" TO "name";
ALTER TABLE "column" RENAME COLUMN "title" TO "name";
