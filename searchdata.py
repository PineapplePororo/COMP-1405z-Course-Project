from crawler import dict
import matmult
import math

# alvina
def get_outgoing_links(url):

    '''
    returns a list of other URLs that the page with the given URL links to
    
    '''
    pass


# alvina
def get_incoming_links(url):

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