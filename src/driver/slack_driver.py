import os
import json
from output.slack_output_data import SlackOutputData
from src.interface.driver.slack_driver import SlackDriver
from dataclasses import asdict
import requests


SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


class SlackDriverImpl(SlackDriver):
    def post(self, slack_output: SlackOutputData):
        payload = asdict(slack_output)
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
