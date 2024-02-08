from datetime import datetime
from random import randint
import json
from config_loader import config

class Event:
    def __init__(self):
        self.reporter_id = config["Event"]["initial_reporter_id"]
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.metric_id = randint(config["Event"]["min_metric_id"], config["Event"]["max_metric_id"])
        self.metric_value = randint(config["Event"]["min_metric_id"], config["Event"]["max_metric_value"])
        self.message = config["Event"]["message"]

    def to_json(self):
        """
        Converts the Event object to a JSON string.

        Returns:
        - str: The JSON representation of the Event.
        """
        try:
            return {
                "reporterId": self.reporter_id,
                "timestamp": self.timestamp,
                "metricId": self.metric_id,
                "metricValue": self.metric_value,
                "message": self.message,
            }
            
        except json.JSONDecodeError as e:
            # Handle JSON serialization errors
            raise RuntimeError(f"Error converting Event to JSON: {e}")
