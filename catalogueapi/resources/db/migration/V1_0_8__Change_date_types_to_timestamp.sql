ALTER TABLE "public".draft ALTER date_start type TIMESTAMP USING date_start::TIMESTAMP;
ALTER TABLE "public".draft ALTER date_end type TIMESTAMP USING date_end::TIMESTAMP;
ALTER TABLE "public".draft ALTER creation_date type TIMESTAMP USING creation_date::TIMESTAMP;
ALTER TABLE "public".draft ALTER publication_date type TIMESTAMP USING publication_date::TIMESTAMP;
ALTER TABLE "public".draft ALTER revision_date type TIMESTAMP USING revision_date::TIMESTAMP;
ALTER TABLE "public".draft ALTER metadata_date type TIMESTAMP USING metadata_date::TIMESTAMP;
ALTER TABLE "public".draft ALTER created_at type TIMESTAMP USING created_at::TIMESTAMP;
ALTER TABLE "public".draft ALTER submitted_at type TIMESTAMP USING submitted_at::TIMESTAMP;
ALTER TABLE "public".draft ALTER accepted_at type TIMESTAMP USING accepted_at::TIMESTAMP;

ALTER TABLE "public".item ALTER date_start type TIMESTAMP USING date_start::TIMESTAMP;
ALTER TABLE "public".item ALTER date_end type TIMESTAMP USING date_end::TIMESTAMP;
ALTER TABLE "public".item ALTER creation_date type TIMESTAMP USING creation_date::TIMESTAMP;
ALTER TABLE "public".item ALTER publication_date type TIMESTAMP USING publication_date::TIMESTAMP;
ALTER TABLE "public".item ALTER revision_date type TIMESTAMP USING revision_date::TIMESTAMP;
ALTER TABLE "public".item ALTER metadata_date type TIMESTAMP USING metadata_date::TIMESTAMP;
ALTER TABLE "public".item ALTER created_at type TIMESTAMP USING created_at::TIMESTAMP;
ALTER TABLE "public".item ALTER submitted_at type TIMESTAMP USING submitted_at::TIMESTAMP;
ALTER TABLE "public".item ALTER accepted_at type TIMESTAMP USING accepted_at::TIMESTAMP;

ALTER TABLE "public".history ALTER date_start type TIMESTAMP USING date_start::TIMESTAMP;
ALTER TABLE "public".history ALTER date_end type TIMESTAMP USING date_end::TIMESTAMP;
ALTER TABLE "public".history ALTER creation_date type TIMESTAMP USING creation_date::TIMESTAMP;
ALTER TABLE "public".history ALTER publication_date type TIMESTAMP USING publication_date::TIMESTAMP;
ALTER TABLE "public".history ALTER revision_date type TIMESTAMP USING revision_date::TIMESTAMP;
ALTER TABLE "public".history ALTER metadata_date type TIMESTAMP USING metadata_date::TIMESTAMP;
ALTER TABLE "public".history ALTER created_at type TIMESTAMP USING created_at::TIMESTAMP;
ALTER TABLE "public".history ALTER submitted_at type TIMESTAMP USING submitted_at::TIMESTAMP;
ALTER TABLE "public".history ALTER accepted_at type TIMESTAMP USING accepted_at::TIMESTAMP;
ALTER TABLE "public".history ALTER deleted_at type TIMESTAMP USING deleted_at::TIMESTAMP;

ALTER TABLE "public".harvest ALTER date_start type TIMESTAMP USING date_start::TIMESTAMP;
ALTER TABLE "public".harvest ALTER date_end type TIMESTAMP USING date_end::TIMESTAMP;
ALTER TABLE "public".harvest ALTER creation_date type TIMESTAMP USING creation_date::TIMESTAMP;
ALTER TABLE "public".harvest ALTER publication_date type TIMESTAMP USING publication_date::TIMESTAMP;
ALTER TABLE "public".harvest ALTER revision_date type TIMESTAMP USING revision_date::TIMESTAMP;
ALTER TABLE "public".harvest ALTER metadata_date type TIMESTAMP USING metadata_date::TIMESTAMP;
ALTER TABLE "public".harvest ALTER created_at type TIMESTAMP USING created_at::TIMESTAMP;
ALTER TABLE "public".harvest ALTER submitted_at type TIMESTAMP USING submitted_at::TIMESTAMP;
ALTER TABLE "public".harvest ALTER accepted_at type TIMESTAMP USING accepted_at::TIMESTAMP;