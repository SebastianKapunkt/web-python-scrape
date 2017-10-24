import requests
import os
import json
from bs4 import BeautifulSoup


class Spiegel_online_scrape:
    def __init__(self):
        self.assets_folder = 'assets'
        self.teaser_file = 'teaser.json'
        self.root_url = 'http://www.spiegel.de'

    def request_and_convert(self, url):
        request = requests.get(url)
        return BeautifulSoup(request.text, "html.parser")

    def scrape_article_as_json(self, teaser_list_url):
        soup = self.request_and_convert(teaser_list_url)
        teaser_content = soup.find_all("p", {"class" : "article-intro"})
        
        teaser_json = []
        for article in teaser_content:
            teaser_json.append(self.scrap_teaser_content(article))
        return teaser_json

    def scrap_teaser_content(self, teaser_article):
        author = teaser_article.find_next("span", {"class" : "author"}).text.strip()
        link = ''.join(teaser_article.find_next("a", href=True)['href'])
        title = teaser_article.find_next("a")['title']
        content = self.scrape_article_content(self.root_url + link)
        return {
                'author': author,
                'link': link,
                'title': title,
                'content': content
            }

    def scrape_article_content(self, article_url):
        soup = self.request_and_convert(article_url)
        content = soup.find_all("div", {"class" : "article-section"})[0]
        clear = content.find_all("p", recursive=False)
        obfuscated_p_tags = content.find_all("p", {"class" : "obfuscated"})
        obfuscated_tag_content = []
        clear_tag_content = []
        for clear_text in clear:
            clear_tag_content.append(clear_text.text.strip())

        for obfuscated_p_tag in obfuscated_p_tags:
            text = obfuscated_p_tag.text.strip()
            deobfuscated = []
            for character in text:
                if character.isspace():
                    deobfuscated.append(' ')
                else:
                    deobfuscated.append(chr(ord(character) -1))
            obfuscated_tag_content.append(''.join(deobfuscated))

        return ' '.join(clear_tag_content).join(obfuscated_tag_content)

    def write_json_to_file_in_assets(self, file_name, json_to_save):
        file_path = os.path.join(self.assets_folder, file_name)
        if not os.path.exists(self.assets_folder):
            os.makedirs(self.assets_folder)

        with open(file_path, mode='w') as json_file:
            json_file.write(json.dumps(json_to_save, indent=2))
