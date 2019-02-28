from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import argparse
import pandas as pd
from datetime import datetime, date

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def get_deck_meta(list_url):

    column_map = [
        {"col_number": 0, "field": "strong", "position": 0, "output_name": "finishing_position"}
        , {"col_number": 1, "field": "strong", "position": 0, "output_name": "deck_name"}
        , {"col_number": 1, "field": "a", "position": 0, "output_name": "url"}
        , {"col_number": 1, "field": "strong", "position": 1, "output_name": "created_by"}
        , {"col_number": 2, "field": None, "position": 0, "output_name": "deck_type"}
        , {"col_number": 4, "field": "strong", "position": 0, "output_name": "tournament"}
        , {"col_number": 6, "field": "strong", "position": 0, "output_name": "date"}
        ]

    # Initialize Output object
    metadata = []

    # Determine base URL
    base_url = list_url[0:(list_url[(list_url.find("/") + 2):].find("/") + list_url.find("/") + 2)]

    # Get page HTML
    raw_html = simple_get(list_url)
    if raw_html is not None:
        html = BeautifulSoup(raw_html, 'html.parser')

        # Cycle through rows getting links
        table_rows = html.select('tr')[1:]
        for row in table_rows:
            columns = row.select('td')
            output_row = {}
            for col in column_map:
                if col["field"] == 'strong':
                    value = columns[col["col_number"]].select(col["field"])[col["position"]].text.strip()
                elif col["field"] == 'a':
                    value = base_url + columns[col["col_number"]].select(col["field"])[col["position"]].get('href')
                else:
                    value = columns[col["col_number"]].text.strip()

                output_row[col['output_name']] = value

            metadata.append(output_row)

    return metadata

def get_deck_data(deck_meta):

    # Initialize output object
    output = []

    # Get deck page html
    raw_html = simple_get(deck_meta['url'])
    if raw_html is not None:
        html = BeautifulSoup(raw_html, 'html.parser')

        # Get decklist element from the page
        for ta in html.select('textarea'):
            if ta['id'] == html_id:
                deck_list = ta.text

        # Process text
        d_list = deck_list.split("\n")


        for line in d_list:
            if len(re.sub(r'[^\w]', '', line)) > 0:
                copies = int(line[0:(line.find(' ') + 1)])
                card_name = line[(line.find(' ')+1):line.find('(')]
                output.append({
                    "deck_name": deck_meta['deck_name']
                    , "created_by": deck_meta['created_by']
                    , "tournament": deck_meta['tournament']
                    , "finishing_position": deck_meta['finishing_position']
                    , "deck_type": deck_meta['deck_type']
                    , "date": deck_meta['date']
                    , "url": deck_meta['url']
                    , "card": card_name.strip()
                    , "copies": copies
                    })

    return output

if __name__ == '__main__':

    # Set up argparser
    parser = argparse.ArgumentParser()
    parser.add_argument("format", help="the competition format to scrape")
    parser.add_argument("pages", help="number of pages to scrape", type=int)
    args = parser.parse_args()

    # Get base URL to use
    list_url = "https://mtgdecks.net/" + args.format + "/decklists"

    print("Scraping %d page(s) from %s" % (args.pages, list_url))

    output = []
    pages = args.pages
    html_id = "arena_deck"

    for i in range(pages):
        print("Processing page %d" % (i+1))
        # Get all deck urls on current page
        deck_meta = get_deck_meta(list_url + "/page:" + str(i))

        for deck in deck_meta[0:]:

            # Get the list of cards in each deck
            deck_items = get_deck_data(deck)
            output += deck_items

    # Convert to DataFrame
    output_df = pd.DataFrame(output)

    # Cleanup columns
    output_df['created_by'] = output_df['created_by'].apply(lambda x: x[3:].strip())
    output_df['date'] = output_df['date'].apply(lambda x: datetime.strptime(re.sub(r"[^\w]", "", x), '%d%b%Y'))

    output_df.to_csv('./app/static/data/public/' + (args.format).lower() + '_deck_data.csv')
