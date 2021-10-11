DROP TABLE IF EXISTS "public".asset_in_bundle;

CREATE TABLE "public".asset_in_bundle(
    "asset_id"          character varying NOT NULL,
    "bundle_id"         character varying NOT NULL,
CONSTRAINT pk_asset_in_bundle PRIMARY KEY (asset_id, bundle_id)
);

CREATE INDEX  idx_asset_in_bundle_asset_id ON "public".asset_in_bundle USING btree ("asset_id");