from urllib.request import urlopen
import threading
from queue import Queue
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlparse
import os

def create_project_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_data_files(project_name, base_url):
    queue = project_name + "/queue.txt"
    crawled = project_name + "/crawled.txt"
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled,'')

def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

def delete_file_contents(path):
    with open(path,'w'):
        pass

def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n',''))
    return results

def set_to_file(links, file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file,link)
        append_to_file(file,link)


def get_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''

def get_domain_name2(url):
    try:
        results = get_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''



links = set()


def link_finder(html):
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.findAll('a',href=True):
        link = a['href']
        links.add(link)



class spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        spider.project_name = project_name
        spider.base_url = base_url
        spider.domain_name = domain_name
        spider.queue_file = spider.project_name + '/queue.txt'
        spider.crawled_file = spider.project_name + '/crawled.txt'
        self.boot(self)
        self.crawl_page('first spider', spider.base_url)

    @staticmethod
    def boot(self):
        create_project_dir(spider.project_name)
        create_data_files(spider.project_name,spider.base_url)
        spider.queue = file_to_set(spider.queue_file)
        spider.crawled = file_to_set(spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in spider.crawled:
            print(thread_name + ' crawling ' + page_url)
            print('queue ' + str(len(spider.queue)) + ' | crawled ' + str(len(spider.crawled)))
            spider.add_links_to_queue(spider.gather_link(page_url))
            print(spider.queue)
            try:
                spider.queue.remove(page_url)
            except:
                print('test111')
            spider.crawled.add(page_url)
            spider.update_files()

    @staticmethod
    def gather_link(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')
            link_finder(html_string)
        except:
            print('error cant crawl page')
            return set()
        return links

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in spider.queue:
                continue
            if url in spider.crawled:
                continue
            if spider.domain_name not in url:
                continue
            spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(spider.queue, spider.queue_file)
        set_to_file(spider.crawled, spider.crawled_file)


def create_workers():
    for _ in range(number_of_treads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        url = queue.get()
        spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

def create_jobs():
    for link in file_to_set(queue_file):
        queue.put(link)
    queue.join()
    crawl()

def crawl():
    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        create_jobs()

project_name = 'apple'
home_page = 'http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page'
domain_name = get_domain_name2(home_page)
queue_file = project_name + '/queue.txt'
crawled_file = project_name + '/crawled.txt'
number_of_treads = 4
queue = Queue()
spider(project_name,home_page,domain_name)
create_workers()
crawl()
