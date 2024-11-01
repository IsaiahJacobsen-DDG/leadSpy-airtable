from src.airtable.airtable_api import Airtable
from src.aws.s3 import Bucket

bucket = Bucket()

atb = Airtable()


def lambda_handler(event, context) -> object:
    airtable_data = atb.get_data()
    search_terms, skills_search, any_search, title_search = atb.clean_data(airtable_data)
    bucket.write_bucket(bucket_name='leadspy-upwork', file_name='exact-phrase.json', data=search_terms)
    bucket.write_bucket(bucket_name='leadspy-upwork', file_name='skills-search.json', data=skills_search)
    bucket.write_bucket(bucket_name='leadspy-upwork', file_name='any-words.json', data=any_search)
    bucket.write_bucket(bucket_name='leadspy-upwork', file_name='title_search.json', data=title_search)


if __name__ == '__main__':
    lambda_handler('none', 'none')
