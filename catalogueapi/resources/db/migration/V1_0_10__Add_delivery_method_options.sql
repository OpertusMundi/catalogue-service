ALTER TABLE "public".draft ADD IF NOT EXISTS "delivery_method_options" JSONB;
ALTER TABLE "public".item ADD IF NOT EXISTS "delivery_method_options" JSONB;
ALTER TABLE "public".history ADD IF NOT EXISTS "delivery_method_options" JSONB;
ALTER TABLE "public".harvest ADD IF NOT EXISTS "delivery_method_options" JSONB;