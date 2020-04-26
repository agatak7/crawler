from link_finder import linkFinder
from urllib.request import urlopen
from general import *
from keyword_finder import find_words


class Spider:
    project = ''
    base_url = ''
    domain = ''

    c_file = ''
    q_file = ''
    interest_file = ''

    queue = set([])
    crawl = set([])
    keywords = ''
    threshold = 0

    def __init__(self, project, base_url, keywords, threshold):
        Spider.project = project
        Spider.domain = ''
        Spider.base_url = base_url

        Spider.q_file = Spider.project + '/queue.txt'
        Spider.c_file = Spider.project + '/crawled.txt'
        Spider.interest_file = Spider.project + '/interest.txt'

        Spider.crawl = set()
        Spider.queue = set()
        Spider.keywords = keywords
        Spider.threshold = threshold

        self.boot()
        self.crawl_page("initial spider", Spider.base_url)

    @staticmethod
    def boot():
        create_dir(Spider.project)
        create_data_files(Spider.project, Spider.base_url)
        Spider.queue = links_set(Spider.q_file)
        Spider.crawl = links_set(Spider.c_file)

    @staticmethod
    def crawl_page(thread, url):
        if url not in Spider.crawl:
            if find_words(Spider.keywords, url, Spider.threshold):
                print("interesting words found!")
                append_file(Spider.interest_file, url)
                print(thread + " crawling: " + url)
                print('Queue: ' + str(len(Spider.queue)) + ' Crawled: ' + str(len(Spider.crawl)))
                Spider.add_to_queue(Spider.get_links(url))
                Spider.queue.remove(url)
                Spider.crawl.add(url)
                Spider.update_files()


    @staticmethod
    def get_links(url):
        html_string = ''
        result = set()
        try:
            response = urlopen(url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = linkFinder(Spider.base_url, url)
            finder.feed(html_string)
            result = finder.get_links()
        except Exception as e:
            print("error connecting to " + url + " " + str(e))
        return result

    @staticmethod
    def add_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawl):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_file(Spider.q_file, Spider.queue)
        set_file(Spider.c_file, Spider.crawl)
