import math
import os
import json

dict = json.load(open(os.path.join('crawl', "dict.json"), "r"))
reverseDict = json.load(open(os.path.join('crawl', "reverseDict.json"), "r"))

# returns a list of other URLs that the page with the given URL links to
def get_outgoing_links(url):

    # if the url wasn't found in the crawling process
    if url not in dict:
        return None

    list = []

    # retrieve the name of the folder of the specific url
    folderName = dict[url]    

    # find the path to the folder
    folderPath = os.path.join('crawl', folderName)

    # find the path to the url file
    urlFilePath = os.path.join(folderPath, "urls")

    # open file
    urls = open(urlFilePath, "r")

    for link in urls:
        # add every url to list
        list.append(link.strip())

    return list


# returns a list of URLs for pages that link to the page with the given URL
def get_incoming_links(url):

    # a list of urls for pages that link to the given url
    list = []

    # store the list of all folders in crawl
    folders = os.listdir("crawl")

    for folder in folders:
        # find the path to the url file
        urlFilePath = os.path.join(os.path.join("crawl", folder), "urls")

        # open the url folder
        urls = open(urlFilePath, "r")

        # check every link to see if it matches the given url
        for link in urls:
            if url == link.strip():
                # matched; add the url of this file's owner to list
                list.append(reverseDict[int(folder.split("_")[0])])
                break

    # if given url was not found during was not found
    if (len(list) == 0):
        return None

    return list


# omar
def get_page_rank(url):

    '''
    returns the pagerank value of the page with that url

    watch lecture video
    alpha value of 0.1
    Euclidean distance
    
    '''
    
    pass


# returns the inverse document frequency of that word within the crawled pages
def get_idf(word):

    # count of documents word appears in
    count = 0

    # store the list of all folders in crawl
    folders = os.listdir("crawl")

    for folder in folders:
        # find the path to the word file
        wordFilePath = os.path.join(os.path.join("crawl", folder), "words")

        # open the url folder
        words = open(wordFilePath, "r")

        # check every link to see if it matches the given url
        for w in words:
            if word == w.strip():
                # matched; increment count
                count += 1
                break

    # if given url was not found during was not found
    if (count == 0):
        return 0

    return math.log((len(dict)/(1+count)), 2)


# return the term frequency of that word within the page with the given URL
def get_tf(url, word):

    # if the url wasn't found in the crawling process
    if url not in dict:
        return 0

    # count of number of occurences of w in file
    wordCount = 0
    # count of total number of words
    totalCount = 0

    # retrieve the name of the folder of the specific url
    folderName = dict[url]    

    # find the path to the folder
    folderPath = os.path.join('crawl', folderName)

    # find the path to the url file
    wordFilePath = os.path.join(folderPath, "words")

    # open file
    words = open(wordFilePath, "r")

    # for every word in the file check if it matches with the given word
    for w in words:
        if w.strip() == word:
            # matched; increment 
            wordCount += 1
        # increment total count of words in file
        totalCount += 1

    # if the given word does not appear in the page 
    if (wordCount == 0):
        return 0

    return wordCount/totalCount
    

# return the tf-idf weight for the given word within the page represented by the given URL
def get_tf_idf(url, word):
    return math.log(1+get_tf(url, word), 2)*get_idf(word)


'''
# test cases:

# 2 3 4 5 6 7 8 9
s0 = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"
# 1  
s1 = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-1.html"
# 1 9 10
s8 = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-8.html"

# print(get_outgoing_links(s0))

# # total kiwi : 7
# print(get_idf("none"))

# # s0, coconut = 3/23
# print(get_tf(s0, "none"))

# # kiwi; idf: log(10/1+7) tf: 2/23
# print(get_tf_idf(s0, "kiwi"))
'''


