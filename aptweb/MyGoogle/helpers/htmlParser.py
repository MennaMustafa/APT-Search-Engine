import re
from urlparse import urljoin
from HTMLParser import HTMLParser
from collections import OrderedDict
from help_functions import generalize_data

incomplete = re.compile('&[a-zA-Z#]')
entityref = re.compile('&([a-zA-Z][-.a-zA-Z0-9]*)[^a-zA-Z0-9]')
charref = re.compile('&#(?:[0-9]+|[xX][0-9a-fA-F]+)[^0-9a-fA-F]')
starttagopen = re.compile('<[a-zA-Z]')


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__ignoreNextData = False
        # ignore the data just if that's a script, style, base, link or noscript. Also ignore meta tags that don't have the arrtibute name =author, keywords or description
        self.__ignoredTags = ['script', 'style', 'base', 'link', 'noscript']
        self.__acceptedMetaTags = ['description', 'author', 'keywords']
        self.__ignoredWords = ['an', 'the']
        self.__pageInfo = dict()
        self.__fileSet = set()
        self.__allWords = list()
        self.__allRanks = list()
        self.__wordsDictionary = OrderedDict()
        self.__currentIsHyperLink = False
        self.__currentIsTitle = False
        self.firstComment = True
        self.__currentPositionWeight = 3
        self.__out_links = list()

    def index_this_page(self, pagePath):
        self.__currentIsHyperLink = False
        self.__currentIsTitle = False
        self.firstComment = True
        self.__currentPositionWeight = 3
        self.__fileSet.clear()
        self.__allWords = list()
        self.__allRanks = list()
        self.__out_links = list()
        self.__wordsDictionary = dict()
        page = open(pagePath, 'r').read().lower()
        self.feed(page)
        num = 0
        for word in sorted(self.__fileSet):
            num += 1
            indexes = [index for index, x in enumerate(self.__allWords) if x == word]
            rank = sum([self.__allRanks[index] for index in indexes])
            self.__wordsDictionary[word] = (indexes, rank)
        if num != len(self.__wordsDictionary):
            print "Error"
        print pagePath + " --> " + str(len(self.__wordsDictionary))
        self.__pageInfo["words_dictionary"] = self.__wordsDictionary.copy()
        self.__pageInfo["out_links"] = self.__out_links
        return self.__pageInfo

    # overwrite the feed function to just overwrite old rawdata by new data, but not to concatenate them
    def feed(self, data):
        """Feed data to the parser.
        the overwritten function is just overwrite old rawdata by new data, but not to concatenate them as the original function does
        """
        self.rawdata = data
        self.goahead(0)

    # overwrite the goahead function to handle the possible exceptions
    def goahead(self, end):
        rawdata = self.rawdata
        i = 0
        n = len(rawdata)
        while i < n:
            try:
                match = self.interesting.search(rawdata, i)  # < or &
                if match:
                    j = match.start()
                else:
                    j = n
                if i < j: self.handle_data(rawdata[i:j])
                i = self.updatepos(i, j)
                if i == n: break
                startswith = rawdata.startswith
                if startswith('<', i):
                    if starttagopen.match(rawdata, i):  # < + letter
                        k = self.parse_starttag(i)
                    elif startswith("</", i):
                        k = self.parse_endtag(i)
                    elif startswith("<!--", i):
                        k = self.parse_comment(i)
                    elif startswith("<?", i):
                        k = self.parse_pi(i)
                    elif startswith("<!", i):
                        k = self.parse_declaration(i)
                    elif (i + 1) < n:
                        self.handle_data("<")
                        k = i + 1
                    else:
                        break
                    if k < 0:
                        if end:
                            self.error("EOF in middle of construct")
                        break
                    i = self.updatepos(i, k)
                elif startswith("&#", i):
                    match = charref.match(rawdata, i)
                    if match:
                        name = match.group()[2:-1]
                        self.handle_charref(name)
                        k = match.end()
                        if not startswith(';', k - 1):
                            k = k - 1
                        i = self.updatepos(i, k)
                        continue
                    else:
                        if ";" in rawdata[i:]:  # bail by consuming &#
                            self.handle_data(rawdata[0:2])
                            i = self.updatepos(i, 2)
                        break
                elif startswith('&', i):
                    match = entityref.match(rawdata, i)
                    if match:
                        name = match.group(1)
                        self.handle_entityref(name)
                        k = match.end()
                        if not startswith(';', k - 1):
                            k = k - 1
                        i = self.updatepos(i, k)
                        continue
                    match = incomplete.match(rawdata, i)
                    if match:
                        # match.group() will contain at least 2 chars
                        if end and match.group() == rawdata[i:]:
                            self.error("EOF in middle of entity or char ref")
                        # incomplete
                        break
                    elif (i + 1) < n:
                        # not the end of the buffer, and can't be confused
                        # with some other construct
                        self.handle_data("&")
                        i = self.updatepos(i, i + 1)
                    else:
                        break
                else:
                    assert 0, "interesting.search() lied"
            except:
                i += 1
        # end while
        if end and i < n:
            self.handle_data(rawdata[i:n])
            i = self.updatepos(i, n)
        self.rawdata = rawdata[i:]

    def handle_comment(self, data):
        if self.firstComment:
            self.__pageInfo["link"] = data.strip(' ')
            self.firstComment = False

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.__currentPositionWeight -= 1
            self.__ignoreNextData = False
        elif tag in self.__ignoredTags:
            self.__ignoreNextData = True
        elif tag == "meta":
            attrs = dict(attrs)
            if "name" in attrs.keys() and attrs['name'] in self.__acceptedMetaTags:
                self.handle_data(attrs['content'])
        elif tag == "a":
            self.__currentIsHyperLink = True
            out_link = dict(attrs)["href"]
            x = urljoin(self.__pageInfo["link"], out_link).strip(" \n")
            if str(x).startswith("http") and x not in self.__out_links and x != self.__pageInfo["link"]:
                self.__out_links.append(x)
        elif tag == "title":
            self.__currentIsTitle = True

    def handle_endtag(self, tag):
        if (tag == "h1" or tag == "h2") and self.__currentPositionWeight == 2:
            self.__currentPositionWeight -= 1
        elif tag == "a":
            self.__currentIsHyperLink = False
        elif tag == "head" or tag in self.__ignoredTags:
            self.__ignoreNextData = False
        elif tag == "title":
            self.__currentIsTitle = False

    def handle_data(self, data):
        # stringfy the data
        data = str(data)
        if not self.__ignoreNextData:
            if self.__currentIsTitle:
                self.__pageInfo["title"] = data
            data = generalize_data(data)
            # split the data and add the words to the list
            for word in data.split():
                # check if it's not in the __ignoredWords and is alphanumeric that has at least one character
                if word not in self.__ignoredWords and re.match(r'^\d*[a-z][a-z0-9]+$', word):
                    if self.__currentIsHyperLink:
                        self.__allRanks.append(5)
                    else:
                        self.__allRanks.append(self.__currentPositionWeight * 5)
                    self.__allWords.append(word)
                    self.__fileSet.add(word)
