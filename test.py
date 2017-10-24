from scrape import Spiegel_online_scrape

def run():
    s = Spiegel_online_scrape()
    json = s.scrape_article_as_json('http://www.spiegel.de/spiegelplus/')
    s.write_json_to_file_in_assets(s.teaser_file, json)
   
if __name__ == '__main__':
    run()
