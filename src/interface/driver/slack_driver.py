from abc import ABCMeta, abstractmethod
from output.slack_output_data import SlackOutputData


class SlackDriver(metaclass=ABCMeta):
    @abstractmethod
    def post(self, slack_output: SlackOutputData):
        raise NotImplementedError
