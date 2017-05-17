from crawler import Crawler
from indexer import MyIndexer
#import os
import time

class AppManager:

    def __init__(self, seeds):
        self.__seed = seeds
        self.__crawlers = []
        #self.__indexers = []
        self.__files = []

    def start_crawling(self):
        n = int(input("Enter Number of threads (maximum is "+ str(len(self.__seed)) + "): "))
        n = min(n, len(self.__seed))
        print "Number of crawlers is set to " + str(n)
        stopCondition = int(input("Enter Number of pages to crawl"))
        Crawler.update_crawler_options(stopCondition)
        numOfSeedsPerCrawler = len(self.__seed) / n
        for i in range(0, n):
            self.__crawlers.append(Crawler(i, "Thread-" + str(i)))
            if i == n-1:
                end = len(self.__seed)
            else:
                end = (i+1)*numOfSeedsPerCrawler
            print "This crawler will search from " + str(i*numOfSeedsPerCrawler) + " to " + str(end)
            for j in range(i*numOfSeedsPerCrawler, end):
                self.__crawlers[i].add_seed(self.__seed[j])
            self.__crawlers[i].start()
        for i in range(0, n):
            self.__crawlers[i].join()

    def start_indexing(self, filesPath):
        startTime = time.clock()
        indexer = MyIndexer(filesPath)
        indexer.index_files()
        endTime = time.clock()
        print "it took the indexer " + str(endTime - startTime) + " to finish "
