# Name: Grecia Alvarado
# Assignment 3 problem 4
from bs4 import BeautifulSoup
from pymongo import MongoClient
import ssl
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import urllib

class Frontier:
    def __init__(self, start_url):
        self.queue = [start_url] #bfs-like search
        self.visited = set() #don't revisist urls

    def add_url(self, url):
        if url not in self.visited and url not in self.queue:
            self.queue.append(url)

    def next_url(self):
        if len(self.queue) != 0:
            url = self.queue.pop(0)
            # mark as visited!!
            self.visited.add(url)
            return url
        else:
            return None

    def done(self):
        return len(self.queue) == 0

def retrieve_url(url):
    try:
        #concat w/ relative
        entireURL = urllib.parse.urljoin("https://www.cpp.edu/sci/computer-science/", url)
        unverified = ssl._create_unverified_context()
        return urlopen(entireURL, context=unverified).read().decode('utf-8')
    except HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        return None
    except URLError as e:
        print(f"URL Error: {e.reason}")
        return None

def store_page(url, html):
    client = MongoClient()
    db = client.crawler_info
    pages = db.pages
    document = {
        "URL": url,
        "HTML": html
    }
    pages.insert_one(document)
    print(f"stored: {url}")

def target_page(html):
    bs = BeautifulSoup(html, 'html.parser')
    print(bs.h1)
    heading = bs.find('h1', string='Permanent Faculty')
    return heading is not None

def parse(html):
    bs = BeautifulSoup(html, 'html.parser')
    #get all the links on the page
    links = [a.get('href') for a in bs.find_all('a', href=True)]
    return links

if __name__ == "__main__":
    frontier = Frontier("https://www.cpp.edu/sci/computer-science/")

    while not frontier.done():
        url = frontier.next_url()
        print(f"curr url: {url}")
        html = retrieve_url(url)
        print()
        if html is not None:
            store_page(url, html)
            if target_page(html):
                print("found it!!")
                break 
            else:
                for nextURL in parse(html):
                    frontier.add_url(nextURL)
                    #print(f"looking at {next_url}")
