import threading
from queue import Queue
from spider import Spider
from general import *

PROJECT_NAME = 'art'
HOMEPAGE = 'https://www.in4art.eu/'
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWL_FILE = PROJECT_NAME + '/crawl.txt'
NO_THREADS = 8
KEYWORDS = {'art', 'sculpture', 'innovation'}
THRESHOLD = 2
queue = Queue()
spider = Spider(PROJECT_NAME, HOMEPAGE,KEYWORDS, THRESHOLD)

def create_workers():
    for _ in range(NO_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in links_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = links_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()