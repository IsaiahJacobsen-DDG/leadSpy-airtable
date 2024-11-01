import logging
import os

from pyairtable import Api

from src.slack.slack_error_messages import Slack, slack_error_handler
from dotenv import load_dotenv

load_dotenv()

slack = Slack()


class Airtable:

    def __init__(self):
        self.api = Api(os.getenv('AIRTABLE_API_KEY'))
        self.table = self.api.table(os.getenv('BASE_ID'), os.getenv('TABLE_NAME'))
        self.row_data = []
        self.s3_data = []

    def get_data(self):
        try:
            data = self.table.all()
        except Exception as e:
            logging.error(
                f"Error fetching data from Airtable: {e}, Response: {e.response.text if hasattr(e, 'response') else 'No response data'}")
            slack.send_error(e)
            raise
        return data

    @slack_error_handler
    def clean_data(self, data) -> tuple:
        exact_phrase_search = []
        skills_search = []
        words_any = []
        title_search = []

        for record in data:
            term = record.get('fields').get('Term')
            search_type = record.get('fields').get('SearchType')
            search_package = {"searchTerm": term}

            if search_type == 'The exact phrase':
                exact_phrase_search.append(search_package)
            elif search_type == 'Any of these words':
                words_any.append(search_package)
            elif search_type == 'Title Search':
                title_search.append(search_package)
            else:
                skills_search.append(search_package)

        return exact_phrase_search, skills_search, words_any, title_search


if __name__ == '__main__':
    atb = Airtable()

