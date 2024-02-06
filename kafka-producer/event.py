import datetime
from random import randint
import json
import configparser


# Read configuration from configuration.ini file
config = configparser.ConfigParser()
config.read("configuration.ini")

class Event:
    def __init__(self):
        self.reporter_id = config.getint("event", "initial_reporter_id")
        self.timestamp = datetime.now().strftime(config.get("Event", "timestamp_format"))
        self.metric_id = randint(config.getint("Event", "min_metric_id"), config.getint("Event", "max_metric_id"))
        self.metric_value = randint(config.getint("Event", "min_metric_id"), config.getint("Event", "max_metric_value"))
        self.message = config.get("Event", "message")

    def to_json(self):
        """
        Converts the Event object to a JSON string.

        Returns:
        - str: The JSON representation of the Event.
        """
        try:
            return json.dumps(
                {
                    "reporterId": self.reporter_id,
                    "timestamp": self.timestamp,
                    "metricId": self.metric_id,
                    "metricValue": self.metric_value,
                    "message": self.message,
                }
            )
        except json.JSONDecodeError as e:
            # Handle JSON serialization errors
            raise RuntimeError(f"Error converting Event to JSON: {e}")
