ALTER TABLE "public".draft ADD IF NOT EXISTS "vetting_required" boolean;
ALTER TABLE "public".item ADD IF NOT EXISTS "vetting_required" boolean;
ALTER TABLE "public".history ADD IF NOT EXISTS "vetting_required" boolean;
ALTER TABLE "public".harvest ADD IF NOT EXISTS "vetting_required" boolean;