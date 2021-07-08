import json
from output.slack_output_data import SlackOutputData
from interface.driver.slack_driver import SlackDriver
from dataclasses import asdict
import requests


class SlackDriverImpl(SlackDriver):
    def __init__(self, url: str):
        self.url = url

    def post(self, slack_output: SlackOutputData):
        payload = asdict(slack_output)
        requests.post(self.url, data=json.dumps(payload))
