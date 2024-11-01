import os
import requests
import json

LAMBDA_NAME = 'leadSpy-main'
LAMBDA_URL = 'https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/leadSpy-main'


class Slack:
    """
    Handles all the Slack webhook interactions.
    """

    def __init__(self):
        """
        Initializes the Slack webhook URL.
        """
        self.lambda_url = ''  # lambda url goes here
        self.slack_web_hook_url = os.getenv('SLACK_WEB_HOOK_URL')
        if not self.slack_web_hook_url:
            raise ValueError("Slack Webhook URL is not set in environment variables")

    def send_error(self, error=None) -> None:
        """
        Sends an error message to the Slack channel 'script-alerts'.
        :param self: Object
        :param error: Catches the thrown error.
        :return: None
        """
        code_block = '```'  # Formatting for Slack
        data = {
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f':poop: An error occurred in <{LAMBDA_URL}|{LAMBDA_NAME}> lambda:',
                    },
                },
                {
                    'type': 'divider',
                },
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f'{code_block}{error}{code_block}',
                    },
                },
            ],
        }
        if os.getenv('BRANCH') != 'dev':
            response = requests.post(self.slack_web_hook_url, data=json.dumps(data),
                                     headers={'Content-Type': 'application/json'})
            if response.status_code != 200:
                print(f"Failed to send Slack message: {response.status_code} {response.text}")
            else:
                print("Message sent to Slack successfully!")


def slack_error_handler(func):
    """
    A decorator used for handling errors and sending them to Slack.

    :param func: The function to wrap.
    :return: The wrapper function.
    """
    slack = Slack()

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            print('Slack Error Raised \n', error)
            slack.send_error(str(error))  # Send error message to Slack
            raise

    return wrapper


if __name__ == '__main__':
    s = Slack()
