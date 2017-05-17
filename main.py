from appManager import AppManager
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
mainPages = ["http://www.w3schools.com/", "https://en.wikipedia.org/wiki/Main_Page", "http://www.dmoztools.net/", "http://www.independent.co.uk/", "http://sciencemag.org/"]
myAppManager = AppManager(mainPages)
myAppManager.start_crawling()
print "Finished Crawling"
myAppManager.start_indexing("files/")
print "Finished Indexing"
