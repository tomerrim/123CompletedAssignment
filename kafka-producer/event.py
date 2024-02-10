from datetime import datetime
from random import randint
from config_loader import config
from logger import logger

class Event:
    def __init__(self):
        self.reporter_id = config["Event"]["initial_reporter_id"]
        self.timestamp = datetime.now().strftime(config["Event"]["timestamp_format"])
        self.metric_id = randint(config["Event"]["min_metric_id"], config["Event"]["max_metric_id"])
        self.metric_value = randint(config["Event"]["min_metric_id"], config["Event"]["max_metric_value"])
        self.message = config["Event"]["message"]

    def to_dict(self):
        """
        Converts the Event object to a Python dictionary suitable for JSON serialization.

        Returns:
        - dict: The dictionary representation of the Event.
        """
        try:
            return {
                "reporterId": self.reporter_id,
                "timestamp": self.timestamp,
                "metricId": self.metric_id,
                "metricValue": self.metric_value,
                "message": self.message,
            }

        except Exception as e:
            logger.exception(f"Error converting Event to dictionary: {e}")
            raise RuntimeError(f"Error converting Event to dictionary: {e}")
