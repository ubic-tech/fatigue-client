cat create-tables.sql | docker run -i --rm --network="host" yandex/clickhouse-client -mn
python main.py --drivers=5 | docker run -i --rm --network="host" yandex/clickhouse-client --query="INSERT INTO default.drivers FORMAT CSV"
