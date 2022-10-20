from crawler import dict
import matmult
import math
import os


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


# alvina
def get_incoming_links(url):

    # a lsit of urls for pages that link to the given url
    list = []

    # store the list of all folders in crawl
    folders = os.listdir("crawl")

    for folder in folders:
        # find the path to the url file
        urlFilePath = os.path.join(os.path.join("crawl", folder), "urls")

        urls = open(urlFilePath, "r")

        # for link in urls:
        #     if link == url:


    '''
    returns a list of URLs for pages that link to the page with the given URL
    
    - folders = os.listdir("crawl")
    - for folder in folders:
        os.path.join(folder, "url")

        go through each line check if url is in the file

    '''
    pass

# omar
def get_page_rank(url):

    '''
    returns the pagerank value of the page with that url

    watch lecture video
    alpha value of 0.1
    Euclidean distance
    
    '''
    
    pass

# omar
def get_idf(word):
    
    '''
    returns the inverse document frequency of that word within the crawled pages

    change crawler.py 
    - have dict key: word value: # of doucuments words appear in

    total number of documents - len(dict)
    '''
    pass

# omar
def get_tf(url, word):

    '''
    return the term frequency of that word within the page with the given URL
    '''

    pass

# alvina
def get_tf_idf(url, word):

    '''
    return the tf-idf weight for the given word within the page represented by the given URL

    '''
    pass


s = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"

print(get_incoming_links(s))