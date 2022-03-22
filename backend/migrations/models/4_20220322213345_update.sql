-- upgrade --
ALTER TABLE "task" ADD "assignee_id" INT;
ALTER TABLE "task" ADD CONSTRAINT "fk_task_teammemb_13199afa" FOREIGN KEY ("assignee_id") REFERENCES "teammember" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "task" DROP CONSTRAINT "fk_task_teammemb_13199afa";
ALTER TABLE "task" DROP COLUMN "assignee_id";
