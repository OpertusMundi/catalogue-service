ALTER TABLE "public".draft ADD IF NOT EXISTS "parent_data_source_id" character varying;
ALTER TABLE "public".item ADD IF NOT EXISTS "parent_data_source_id" character varying;
ALTER TABLE "public".history ADD IF NOT EXISTS "parent_data_source_id" character varying;
ALTER TABLE "public".harvest ADD IF NOT EXISTS "parent_data_source_id" character varying;