ALTER TABLE "public".draft ADD IF NOT EXISTS "contract_template_type" character varying(64) NOT NULL DEFAULT ('MASTER_CONTRACT');
ALTER TABLE "public".item ADD IF NOT EXISTS "contract_template_type" character varying(64) NOT NULL DEFAULT ('MASTER_CONTRACT');
ALTER TABLE "public".history ADD IF NOT EXISTS "contract_template_type" character varying(64) NOT NULL DEFAULT ('MASTER_CONTRACT');
ALTER TABLE "public".harvest ADD IF NOT EXISTS "contract_template_type" character varying(64) NOT NULL DEFAULT ('MASTER_CONTRACT');