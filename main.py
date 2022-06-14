from itertools import takewhile
from datetime import datetime
import pathlib
import lxml.etree as ET
import requests
import sys

api_url = "https://manifold.markets/api/v0/markets"
limit = 10
etag = pathlib.Path('./etag').read_text().strip()

if etag == '':
    new_etag = requests.get(api_url, params={'limit': '1'}).json()[0]['id']
    with open('etag', 'w') as f:
        f.write(new_etag)
    sys.exit(0)


feed_output_path = './feed.xml'

all_markets = []
before = None
while True:
    response = requests.get(api_url, params={'limit': '10', 'before': before}).json()
    articles = list(takewhile(lambda x: x['id'] != etag, response))
    all_markets += articles

    if len(articles) < limit:
        break

    before = articles[-1]['id']

if len(all_markets) == 0:
    sys.exit(0)


def to_item(market):
    item = ET.Element('item')
    try:
        ET.SubElement(item, 'title').text = f'{market["question"]} - {int(market["probability"]*100)}% - M${int(market["volume"])}'
    except KeyError:
        ET.SubElement(item, 'title').text = f'{market["question"]} - M${int(market["volume"])}'
    ET.SubElement(item, 'description').text = market['description']
    ET.SubElement(item, 'category').text = '/'.join(market['tags'])
    ET.SubElement(item, 'link').text = market['url']
    ET.SubElement(item, 'author').text = market['creatorName']
    ET.SubElement(item, 'pubDate').text = datetime.fromtimestamp(market['createdTime']//1000).strftime("%a, %d %b %Y %H:%M:%S %z")
    ET.SubElement(item, 'guid').text = market['id']

    return item


parser = ET.XMLParser(remove_blank_text=True)
out_tree = ET.ElementTree()
out_tree.parse(feed_output_path, parser)
out_tree_root = out_tree.find('.//channel').find('.//description')
for market in all_markets:
    out_tree_root.addnext(to_item(market))
out_tree.write(feed_output_path, pretty_print=True)

with open('etag', 'w') as f:
    f.write(all_markets[0]['id'])
