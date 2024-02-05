import datetime
import random
import json


class Event:
    def __init__(self, reporter_id):
        self.reporter_id = reporter_id
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.metric_id = random.randint(1, 10)
        self.metric_value = random.randint(1, 100)
        self.message = "HELLO WORLD"

    def to_json(self):
        return json.dumps(
            {
                "reporterId": self.reporter_id,
                "timestamp": self.timestamp,
                "metricId": self.metric_id,
                "metricValue": self.metric_value,
                "message": self.message,
            }
        )
