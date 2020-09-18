cat create-tables.sql | docker run -i --rm --network taxi-net yandex/clickhouse-client --host db -mn
python main.py --drivers=100 | docker run -i --rm --network taxi-net yandex/clickhouse-client --host db --query="INSERT INTO default.drivers FORMAT CSV"
