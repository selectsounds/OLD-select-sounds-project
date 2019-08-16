import re
from typing import Dict

import bs4
import urllib.request


class RecordWebPage:
    # Add Docstring here later

    _page_url = None
    _page_soup = None
    _url_body = None
    change_page_url_flag = None
    change_page_data_flag = None

    _selected_record = None

    def __init__(self, page_url=None, url_body=None):
        """
        :param page_url: Parameter for directly passing in entire page url, rather than the page_url_body
            -> This would be used for creating a new RecordWebPage object using a directly extracted url
        :param url_body: String used to construct main URL (page_url) - example: 'Carl-Douglas-Run-Back/release/1727101'
        """
        if page_url:
            self._page_url = page_url
            self.change_page_data_flag = True

        elif url_body:
            self._url_body = url_body
            self.set_flags_to_true()

    @property
    def site_url(self):
        return 'https://www.discogs.com/'

    @property
    def page_url(self):
        if self.change_page_url_flag:
            self._page_url = self.generate_page_url(self.url_body)
        return self._page_url

    @property
    def url_body(self):
        return self._url_body

    @url_body.setter
    def url_body(self, url_body):
        self._url_body = url_body
        self.set_flags_to_true()

    def set_flags_to_true(self):  # change_page_url_flag=True, page_url_changed=True):

        # # error handling
        # if type(change_page_url_flag) is not bool:
        #     raise ValueError('change_page_url_flag argument must be boolean value, was: "{}"'.
        #                      format(str(type(change_page_url_flag)[8:-2])))
        #
        # # error handling
        # if type(page_url_changed) is not bool:
        #     raise ValueError('page_url_changed argument must be boolean value, was: "{}"'.
        #                      format(str(type(page_url_changed)[8:-2])))

        # flag to allow dynamic updating of page_url when url_body is changed
        self.change_page_url_flag = True

        # flag for allowing dynamic updating of page data when url changed
        self.change_page_data_flag = True

    def generate_page_url(self, *args):
        # page_url = self.site_url + '/'.join(args)

        page_url = self.site_url + self.url_body
        #  self.site_url + \
        # (self.url_body if self.url_body else '')
        # (self.url_prefix if self.url_prefix else '') + \

        # self.change_page_url_flag = False
        return page_url

    @property
    def page_soup(self):
        if self.change_page_data_flag:
            self._page_soup = self.create_record_page_soup()
        return self._page_soup

    def extract_html_data_from_page(self):
        print("connecting to web page '{}'...".format(self.page_url))

        with urllib.request.urlopen(self.page_url) as http_client:
            html_data = http_client.read()
            http_client.close()

        # logging
        print("successfully connected")

        return html_data

    def create_record_page_soup(self):
        html_data = self.extract_html_data_from_page()

        # logging
        print("converting page url to BeautifulSoup format...")

        page_soup = bs4.BeautifulSoup(html_data, "html.parser")

        # logging
        print("successfully converted")

        self.change_page_data_flag = False
        return page_soup

    @staticmethod
    def check_url_substring(url_substring):
        if not url_substring:
            return ''

        checked_string = url_substring.strip()

        if checked_string[-1] != '/':
            checked_string += '/'

        # Add more to this method as requirements develop
        # Could possibly override with specific requirements in child classes

        return checked_string


class SearchRecordWebPage(RecordWebPage):
    # Add Docstring here later

    _raw_search_results = None
    _search_result_data = None
    change_raw_search_results_flag = None
    change_search_result_data_flag = None

    @property
    def url_prefix(self):
        return 'search'

    # Feature to complete later - dictionary for different search types i.e. genre etc
    # @property
    # def search_type_strings(self):
    #     return {}

    @property
    def url_search_type(self):
        return self._url_search_type

    def __init__(self, url_search_type='?q=', search_str=None, url_record_search_type='release'):
        self._url_search_type = url_search_type
        self._search_str = search_str
        self._url_record_search_type = url_record_search_type

        # Make custom url_body parameter using url_prefix & entered search
        temp_url_body = self.generate_page_url()

        # Pass created temp_url_body parameter into parent constructor
        super(SearchRecordWebPage, self).__init__(url_body=temp_url_body)

    @property
    def search_str(self):
        return self._search_str

    @search_str.setter
    def search_str(self, search_str):
        self._search_str = search_str
        self.set_flags_to_true()

    @property
    def url_body(self):
        return self.url_search_type + \
               self.check_search_substring(self.search_str) + \
               self.url_record_search_type

    def set_flags_to_true(self):
        super(SearchRecordWebPage, self).set_flags_to_true()

        # Flag to extract new raw search results from html data (page_soup)
        self.change_raw_search_results_flag = True

        # Flag to extract search data from raw_search_results
        self.change_search_result_data_flag = True

    @property
    def url_record_search_type(self):
        return 'type=' + self._url_record_search_type

    @url_record_search_type.setter
    def url_record_search_type(self, str_value):
        self._url_record_search_type = str_value

    # @property
    # def page_url(self):
    #     if self.change_page_url_flag:
    #         self._page_url = self.generate_page_url(self.url_prefix,
    #                                                 self.url_search)
    #     return self._page_url

    # def generate_page_url(self):
    #     return super(SearchRecordWebPage, self).generate_page_url([self.url_prefix,
    #                                                               self.url_search_type,
    #                                                               self.url_search,
    #                                                               self.url_record_search_type])

    # page_url = self.site_url + self.url_prefix + self.url_search_type + self.url_search + self.url_record_search_type
    #
    # self.change_page_url_flag = False
    # return page_url

    @property
    def search_results_html_position(self):
        return "div", {"class": "card card_large float_fix shortcut_navigable"}

    @property
    def raw_search_results(self):
        if self.change_raw_search_results_flag or self.change_page_data_flag or self.change_page_url_flag:
            self._raw_search_results = self.extract_raw_search_results()

        return self._raw_search_results

    def extract_raw_search_results(self):
        page_soup = self.page_soup

        # logging
        print("Retrieving search results from current page...")

        search_results_html_position = self.search_results_html_position

        # Possible feature for later - dynamically pass in parameters from raw_search_results_html_position
        raw_search_results = page_soup.findAll(search_results_html_position[0], search_results_html_position[1])

        # logging
        print("Successfully retrieved results")

        self.change_raw_search_results_flag = False
        return raw_search_results

    @staticmethod
    def extract_search_result_name(result_obj):
        search_result_name = result_obj.h4.a["title"]
        return search_result_name

    @staticmethod
    def extract_search_result_artist(result_obj):
        search_result_artist = result_obj.h5.span["title"]
        return search_result_artist

    @staticmethod
    def extract_search_result_image_link(result_obj):
        search_result_image_link = "{img_result}".format(
            img_result=result_obj.a.img["data-src"] if result_obj.a.img else 'N/A')
        if search_result_image_link:
            return search_result_image_link

    @staticmethod
    def extract_search_result_url(result_obj):
        search_result_url = "https://www.discogs.com{}".format(result_obj.h4.a["href"])
        return search_result_url

    def extract_search_result_data(self, number_to_extract=None):
        raw_search_results = self.raw_search_results

        # logging
        print("Extracting (name, artist, image, link) information from search results...")

        search_result_data = []
        if number_to_extract:
            value_to_extract_to = number_to_extract - 1
        else:
            value_to_extract_to = len(raw_search_results)

        for i in range(0, value_to_extract_to):
            result = raw_search_results[i]
            result_name = self.extract_search_result_name(result)
            result_artist = self.extract_search_result_artist(result)
            result_image = self.extract_search_result_image_link(result)
            result_link = self.extract_search_result_url(result)

            search_result_data.append({'name': result_name,
                                       'artist': result_artist,
                                       'image-link': result_image,
                                       'page-link': result_link})

        # logging
        print("Results page extracted")

        self.change_search_result_data_flag = False

        return search_result_data

    @property
    def search_result_data(self):
        if self.change_search_result_data_flag:
            self._search_result_data = self.extract_search_result_data()

        return self._search_result_data

    def select_record(self, index):
        if index < 0 or index > len(self.search_result_data):
            raise ValueError("Index value must be within 0 and 50, was '{}'".format(index))
        elif type(index) is not int:
            raise ValueError("Index must be integer value")

        return self.search_result_data[index]

    @staticmethod
    def check_search_substring(search_str):
        if not search_str:
            return ''

        checked_search_str = search_str.replace(" ", "+")

        if checked_search_str[-1] != '&':
            checked_search_str += '&'

        return checked_search_str

    def generate_search_result_string(self, number_to_extract=None):
        if number_to_extract:
            results_to_display = self.search_result_data[:number_to_extract]

        else:
            results_to_display = self.search_result_data

        # Create string of all found search results and output from function
        return "\n" + "\n\n".join("Result {}:\nName - '{}'\nArtist - '{}'\nImage-link - '{}'\nPage-link - '{}'".
                                  format(index + 1, *result) for index, result in enumerate(results_to_display)) + "\n"

    # Feature to complete later - change page to next page / previous page (separate method)
    # def next_search_results_page(self):


class RecordInfoPage(RecordWebPage):
    # Add Doctype later

    _url_title = None
    _url_suffix = 'release'
    _url_code = None
    _record_data = None
    change_record_data_flag = None

    def __init__(self, page_url=None, url_title=None, url_suffix='release', url_code=None):

        if page_url:
            super(RecordInfoPage, self).__init__(page_url=page_url)
            self.change_record_data_flag = True

        elif url_title and url_suffix and url_code:
            self._url_title = url_title
            self._url_suffix = url_suffix
            self._url_code = url_code
            super(RecordInfoPage, self).__init__(url_body=self.url_body)

        # super(RecordInfoPage, self).__init__(url_body=self.url_body)

    @property
    def url_title(self):
        return self.check_url_title_substring(self._url_title)

    @url_title.setter
    def url_title(self, new_title):
        self._url_title = self.check_url_title_substring(new_title)
        self.set_flags_to_true()

    @property
    def url_body(self):
        return self.url_title + self._url_suffix + "/" + self._url_code

    # def generate_page_url(self):
    #     page_url =

    # @staticmethod
    def check_url_title_substring(self, url_title):
        if not url_title:
            return ''

        checked_url_title = self.check_url_substring(url_title).title().replace(' ', '-').replace("+", "-")

        return checked_url_title

    def extract_record_title(self) -> Dict:
        # insert doctype here

        url_title_span = self.page_soup.find("h1", {"id": "profile_title"}).findAll('span')

        # TODO: Add functionality for records with multiple artists (e.g. https://www.discogs.com/Blaze-Joe-Claussell-Southport-Weekender-Volume2/release/333759)

        # url_title = self.page_soup.find("h1", {"id": "profile_title"})
        #
        # url_title_artist = url_title.findAll("span", {'title': re.compile('.*')})
        # record_artist = ''
        # for a in url_title_artist:
        #     record_artist += a.text.strip()

        # for s in url_title_span_list:

        split_url_title_span_list = [url_title_span[i] for i in range(1, len(url_title_span))]

        record_artist = split_url_title_span_list[0].text.strip().replace("\n", "")
        record_name = split_url_title_span_list[1].text.strip().replace("\n", "")
        return {'name': record_name, 'artist': record_artist}

    def extract_record_label(self):
        return self.page_soup.find("div", {"class": "profile"}).findAll("div", {"class": "content"})[0].a.text

    def extract_record_format_data(self):
        # find second line in record title, containing record form (i.e. Vinyl), size (7" or 12" - optional),
        # speed (in RPM - 33, 45 or 78 - optional) & type (Album, LP / Single / EP)
        rec_format_list = self.page_soup.find("div", {"class": "profile"}).findAll("div", {"class": "content"})[
            1].text.replace(" ", "").replace("\n", "").split(",")

        # TODO: Add functionality for records with extra formatting (e.g. https://www.discogs.com/Blaze-Joe-Claussell-Southport-Weekender-Volume2/release/333759)

        format_types = ['Single', 'EP', 'Album', 'LP']
        speed_types = ['33RPM', '33⅓RPM', '78RPM', '45RPM']
        size_types = ['7"', '10"', '12"']
        rec_format_data = {'format': 'N/A',
                           'speed': 'N/A',
                           'size': 'N/A'}

        for i in rec_format_list:
            if i in format_types:
                rec_format_data['format'] = i

            if i in speed_types:
                rec_format_data['speed'] = i

            if i in size_types:
                rec_format_data['size'] = i

        return rec_format_data

    def extract_record_country(self):
        rec_country = self.page_soup.find("div", {"class": "profile"}).findAll("div", {"class": "content"})[
            2].text.strip().replace("\n", "")
        return rec_country

    def extract_record_release_date(self):
        return self.page_soup.find("div", {"class": "profile"}).findAll("div", {"class": "content"})[
            3].text.strip().replace("\n", "")

    def extract_record_genre(self):
        genre = self.page_soup.find("div", {"class": "profile"}).findAll("div", {"class": "content"})[
            4].text.strip().replace("\n", "")

        style = self.page_soup.find("div", {"class": "profile"}).findAll("div", {"class": "content"})[
            5].text.strip().replace("\n", "")

        if style:
            genre += f', {style}'

        return genre

    def extract_record_price_data(self):
        price_section = self.page_soup.find('div', {'id': 'statistics'})
        if not price_section:
            lowest_price = 0
            median_price = 0
            highest_price = 0

        else:
            price_data = price_section.find("div", {
                "class": "section_content toggle_section_content"}).find("ul", {"class": "last"}).findAll("li")[1:]

            # TODO: Check if price section exists and handle in code

            lowest_price = price_data[0].text.split("\n")[2].strip().replace('£', '')
            lowest_price = float(lowest_price) if lowest_price != '--' else 0.0

            median_price = price_data[1].text.split('\n')[2].strip().replace('£', '')
            median_price = float(median_price) if median_price != '--' else 0.0

            highest_price = price_data[2].text.split('\n')[2].strip().replace('£', '')
            highest_price = float(highest_price) if highest_price != '--' else 0.0

        return {
            'lowest-price': lowest_price,
            'median-price': median_price,
            'highest-price': highest_price
        }

    def extract_record_tracklist(self):
        rec_playlist = self.page_soup.find("table", {"class": "playlist"}).findAll("tr")

        playlist = []

        for tr in rec_playlist:
            if tr.find("td", {"class": re.compile(r"track tracklist_track_title.*")}):
                playlist.append(tr.find("td", {"class": re.compile(r"track tracklist_track_title.*")}).span.text)

        return playlist

        # for track in rec_playlist:
        #     print("Track {}: {}".format(i, track.find("td", {"class": "track tracklist_track_title"}).span.text))
        #     i += 1

    def extract_record_data(self):
        # logging
        print("Generating record list...")

        # record_title = self.extract_record_title()
        # rec_name = record_title.get('')
        # rec_artist, rec_name = self.extract_record_title()
        rec_label = self.extract_record_label()
        rec_country = self.extract_record_country()
        rec_release_date = self.extract_record_release_date()
        rec_genre = self.extract_record_genre()
        # rec_style = self.extract_record_style

        record_data = self.extract_record_title()
        record_data.update(
            {'label': rec_label,
             'country': rec_country,
             'release-date': rec_release_date,
             'genre': rec_genre,
             }
        )

        record_data.update(self.extract_record_format_data())
        record_data['tracklist'] = self.extract_record_tracklist()
        record_data.update(self.extract_record_price_data())

        # logging
        print("Record list generated")

        return record_data

    @property
    def record_data(self):
        if self.change_record_data_flag or self.change_page_data_flag or self.change_page_url_flag:
            self._record_data = self.extract_record_data()
        return self._record_data

    def set_flags_to_true(self):
        super(RecordInfoPage, self).set_flags_to_true()
        self.change_record_data_flag = True


if __name__ == '__main__':
    # test_record_page = RecordWebPage(url_body='Carl-Douglas-Run-Back/release/1727101')
    # print(test_record_page.page_url)
    # test_record_page.url_body = 'Gene-Chandler-Get-Down/release/1258602'
    # print(test_record_page.page_url)
    #
    # test_search_record_page = SearchRecordWebPage(search_str='run back carl douglas')
    # test_search_record_page = SearchRecordWebPage(search_str='Girl I Betcha David Joseph')
    # print(test_search_record_page.page_url)
    # print(test_search_record_page.generate_search_result_string(number_to_extract=5))

    # found_search_result = test_search_record_page.select_record(2)

    # test_search_record_page.search_str = 'gene chandler run back'
    # print(test_search_record_page.page_url)
    # print(test_search_record_page.search_result_data[0])

    # print("\n" + test_search_record.generate_search_result_string())

    test_record_info_page = RecordInfoPage(
        page_url='https://www.discogs.com/Various-Gutta-Butta-Volume-2/release/6548241')
    page_soup = test_record_info_page.page_soup

    # print(test_record_info_page.page_url)
    # print(test_record_info_page.record_data)
    #
    # input('Hello: ')

    # TODO: Implement automated tests to make sure all data is working properly
