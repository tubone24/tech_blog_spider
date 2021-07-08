import json
from output.slack_output_data import SlackOutputData
from interface.driver.slack_driver import SlackDriver
from dataclasses import asdict
import requests
from util.logger import AppLog

_logger = AppLog(__name__)


class SlackDriverImpl(SlackDriver):
    def __init__(self, url: str):
        self.url = url

    def post(self, slack_output: SlackOutputData):
        payload = asdict(slack_output)
        _logger.debug(f"Post Slack: {payload}")
        requests.post(self.url, data=json.dumps(payload))
