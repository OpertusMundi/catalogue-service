DROP INDEX IF EXISTS draft_index;
DROP INDEX IF EXISTS item_index;
DROP INDEX IF EXISTS history_index;
DROP INDEX IF EXISTS harvested_index;

DROP INDEX IF EXISTS ix_draft_resources;
DROP INDEX IF EXISTS ix_item_resources;
DROP INDEX IF EXISTS ix_history_resources;
DROP INDEX IF EXISTS ix_harvest_resources;

DROP INDEX IF EXISTS ix_draft_additional_resources;
DROP INDEX IF EXISTS ix_item_additional_resources;
DROP INDEX IF EXISTS ix_history_additional_resources;
DROP INDEX IF EXISTS ix_harvest_additional_resources;

DROP INDEX IF EXISTS ix_draft_keywords;
DROP INDEX IF EXISTS ix_item_keywords;
DROP INDEX IF EXISTS ix_history_keywords;
DROP INDEX IF EXISTS ix_harvest_keywords;

DROP INDEX IF EXISTS ix_draft_scale;
DROP INDEX IF EXISTS ix_item_scale;
DROP INDEX IF EXISTS ix_history_scale;
DROP INDEX IF EXISTS ix_harvest_scale;

DROP INDEX IF EXISTS ix_draft_open_dataset;
DROP INDEX IF EXISTS ix_item_open_dataset;
DROP INDEX IF EXISTS ix_history_open_dataset;
DROP INDEX IF EXISTS ix_harvest_open_dataset;

DROP INDEX IF EXISTS ix_draft_use_only_for_vas;
DROP INDEX IF EXISTS ix_item_use_only_for_vas;
DROP INDEX IF EXISTS ix_history_use_only_for_vas;
DROP INDEX IF EXISTS ix_harvest_use_only_for_vas;

DROP INDEX IF EXISTS ix_history_deleted;