import scrape
import requests

def run():
    s = scrape.Spiegel_online_scrape()
    teaser_json = s.scrape_teaser_article_as_json('http://www.spiegel.de/spiegelplus/')
    s.write_json_to_file_in_assets(s.teaser_file, teaser_json)

if __name__ == '__main__':
    run()