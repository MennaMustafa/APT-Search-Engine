import time
import re
import threading
import robotparser
import urllib
from urlparse import urlparse, urljoin

_author_ = 'Bassel'


class Crawler(threading.Thread):
    page_count = 0
    visited_pages = []
    stop_condition = 0
    threadLock = threading.Lock()

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.urls = list()
        self.seeds = list()
        self.numOfErrorsForCurrentPage = 0
        self.rp = robotparser.RobotFileParser()

    @classmethod
    def update_crawler_options(cls, stop_condition):
        visitedfile = open("visited.txt", "r")
        sr = visitedfile.read()
        Crawler.visited_pages = sr.splitlines()
        visitedfile.close()
        Crawler.page_count = len(Crawler.visited_pages)
        Crawler.stop_condition = stop_condition

    def add_seed(self, url):
        self.urls.append(url)
        self.seeds.append(url)

    def run(self):
        while len(Crawler.visited_pages) <= Crawler.stop_condition and len(self.urls) > 0:
            url = self.urls[0]
            if (url not in Crawler.visited_pages) or (url in self.seeds):
                # noinspection PyBroadException
                try:
                    self.get_page(url)
                except:
                    self.numOfErrorsForCurrentPage += 1
                    if self.numOfErrorsForCurrentPage > 5:
                        print self.name + ": Too many errors in page " + url
                        self.numOfErrorsForCurrentPage = 0
                        self.urls.remove(url)
                    else:
                        print self.name + ": Error number " + str(self.numOfErrorsForCurrentPage) + " in visiting " + \
                              url + ". I will try again."
                        time.sleep(5)
            else:
                urlindex = Crawler.visited_pages.index(url) + 1
                oldfile = open("files/" + str(urlindex) + ".html", "r")
                oldpage = oldfile.read()
                oldfile.close()
                newpage = bytes("<!-- " + url + " -->\n") + urllib.urlopen(url).read()
                if newpage == oldpage:
                    print(self.name + ": " + url + " already visited with no change")
                    self.urls.remove(url)
                else:
                    print(self.name + ": " + url + " already visited but updated")
                    self.urls.extend(self.get_links(newpage, url))
                    self.urls.remove(url)
                    open("files/" + str(urlindex) + ".html", 'w').close()
                    f = open("files/" + str(urlindex) + ".html", "wb")
                    f.write(newpage)
                    f.close()
                    print(url + " revisited by " + self.name)

    def save_page(self, html_page, url):
        Crawler.page_count += 1
        f = open("files/" + str(Crawler.page_count) + ".html", "wb")
        f.write(bytes("<!-- " + url + " -->\n"))
        f.write(html_page)
        f.close()
        print(url + " Saved by " + self.name)

    def get_page(self, url):
        self.rp.set_url("http://" + urlparse(url).netloc + "/robots.txt")
        self.rp.read()
        if self.rp.can_fetch("*", url):
            print(self.name + ": URL to visit: " + str(url))
            page = urllib.urlopen(url)
            # Critical Section Start
            Crawler.threadLock.acquire()
            if url not in Crawler.visited_pages:
                Crawler.visited_pages.append(url)
            if page.getcode() == 200:
                htmlpage = page.read()
                if url not in Crawler.visited_pages:
                    self.save_page(htmlpage, url)
                    visitedfile = open("visited.txt", "a")
                    visitedfile.write(url + "\n")
                    visitedfile.close()
                Crawler.threadLock.release()
                # Critical Section End
                self.urls.extend(self.get_links(htmlpage, url))
                self.urls.remove(url)
            else:
                Crawler.threadLock.release()
                print("Error Loading " + url)
                self.urls.remove(url)
            self.numOfErrorsForCurrentPage = 0
        else:
            print(self.name + ": " + url + " not allowed by robots.txt")
            self.urls.remove(url)

    def get_links(self, html_page, url):
        matches = re.findall(r'<a[^>]* href="([^"]*)"', html_page)
        links = []
        for link in matches:
            x = urljoin(url, link)
            if str(x).startswith("http"):
                links.append(urljoin(url, link))
        return links


#n = int(input("Enter Number of threads"))
#stop_condition = int(input("Enter Number of pages to crawl"))
#Crawler.update_crawler_options(stop_condition)
#seed = ["http://www.w3schools.com/", "https://en.wikipedia.org/wiki/Main_Page"]
#c = []
#for i in range(0, n):
#    c.append(Crawler(i, "Thread-" + str(i)))
#    c[i].add_seed(seed[i])
#    c[i].start()
#for i in range(0, n):
#    c[i].join()
#print("heeeeeeeeee7 Done")
