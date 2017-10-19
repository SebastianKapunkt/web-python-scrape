import requests
import os
import json
from bs4 import BeautifulSoup


class Spiegel_online_scrape:
    def __init__(self):
        self.assets_folder = 'assets'
        self.teaser_file = 'teaser.json'

    def scrape_teaser_article_as_json(self, teaser_list_url):
        r = requests.get(teaser_list_url)
        soup = BeautifulSoup(r.text, "html.parser")
        teaser_content = soup.find_all("p", { "class" : "article-intro" })

        teaset_json = []

        for teaser_article in teaser_content:
            entry = {
                'author': teaser_article.find_next("span", {"class" : "author"}).text.strip(),
                'link': teaser_article.find_next("a", href=True)['href'],
                'title': teaser_article.find_next("a")['title']
            }
            teaset_json.append(entry)

        return teaset_json;

    def write_json_to_file_in_assets(self, file_name, json_to_save):
        file_path = os.path.join(self.assets_folder, file_name)
        if not os.path.exists(self.assets_folder):
            os.makedirs(self.assets_folder)

        with open(file_path, mode='w') as json_file:
            json_file.write(json.dumps(json_to_save, indent=2))