from typing import List, Dict

from services.recordwebpages import SearchRecordWebPage, RecordInfoPage


def find_record_search_results(record_search: str) -> List[Dict]:
    search_record_web_page = SearchRecordWebPage(search_str=record_search)
    return search_record_web_page.search_result_data[:10]


def extract_record_web_page_data(record_page_url: str) -> Dict:
    record = RecordInfoPage(page_url=record_page_url)

    return record.extract_record_data()

# TODO: Convert recordwebpages.py methods into web_services.py
