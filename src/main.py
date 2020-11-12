import os
import multiprocessing
import json
from py2neo import Graph

neo4j_config_str = os.getenv('NEO4J', '{"host": "localhost"}')
neo4j_config_dict = json.loads(neo4j_config_str)


class Worker(multiprocessing.Process):
    node_count = 100

    def run(self):
        print("'{}' starts".format(self.name))
        g_worker = Graph(**neo4j_config_dict)
        tx_worker = g_worker.begin()
        print("'{}' creates {} Thing nodes".format(self.name, self.node_count))
        for i in range(0, self.node_count):
            tx_worker.run("CREATE (n:Thing) SET n.name = {}".format(i))
        print("'{}' commits".format(self.name))
        tx_worker.commit()
        print("'{}' done".format(self.name))


thing_count = Graph(**neo4j_config_dict).run(
    "MATCH (n:Thing) RETURN count(n) as cnt").data()[0]["cnt"]
print("thing_count before {}".format(thing_count))
worker_1 = Worker()
worker_1.name = "Worker 1"
worker_2 = Worker()
worker_2.name = "Worker 2"
worker_3 = Worker()
worker_3.name = "Worker 3"

worker_1.start()
worker_2.start()
worker_3.start()

worker_2.join()
worker_3.join()
worker_1.join()
thing_count = Graph(**neo4j_config_dict).run(
    "MATCH (n:Thing) RETURN count(n) as cnt").data()[0]["cnt"]
print("thing_count after {}".format(thing_count))
