import webdev

dict = {}
queue = []

def crawl(seed):
    help_crawl(seed)

def help_crawl(url):
    pass

def queueHandling(url):

    global dict
    global queue

    if url not in dict:
        
        # make a new key with a value of 1
        dict[url] = 1


        # pass it to help_crawl






    
	

    

# main
# print(webdev.read_url("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))


