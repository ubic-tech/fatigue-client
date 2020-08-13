# Press Shift+F10 to execute it
from aggregator import Aggregator
from config import AGGREGATORS_DATA
import threading

for data in AGGREGATORS_DATA:
    name, _id, port = data
    aggr = Aggregator(name, _id, port)
    th = threading.Thread(target=aggr.run)
    th.start()
