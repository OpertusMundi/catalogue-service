ALTER TABLE "public".draft ADD IF NOT EXISTS "extensions" jsonb;
ALTER TABLE "public".item ADD IF NOT EXISTS "extensions" jsonb;
ALTER TABLE "public".history ADD IF NOT EXISTS "extensions" jsonb;
ALTER TABLE "public".harvest ADD IF NOT EXISTS "extensions" jsonb;