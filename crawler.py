import webdev



def crawl(seed):
    # keeps track of the pages visited (used for runtime efficiency)
    dict = {}
    # 
    queue = []
    # keeps track of the number of total pages found
    count = 0

    url = seed 
    
    while (len(queue) != 0):

        # extract pp
        # extract url

        # adding to queue 
        # check if the url isn't in queue 
        if url not in dict:
        
            # make a new key of the url
            dict[url] = 0

            # add to end of queue
            queue.append(url)

            # increment count for all succeed crawls
            count += 1







    return count 





# print(webdev.read_url("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))


