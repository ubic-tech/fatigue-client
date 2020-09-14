CREATE TABLE IF NOT EXISTS default.drivers
(
   timestamp DateTime,
   driver String,
   state String
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (driver, timestamp)
SETTINGS index_granularity = 8192;

ALTER TABLE default.drivers DELETE WHERE 1=1

