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

        page = webdev.read_url(url)

        # if there is pp extract pp
        # if there is url extract url
        
        words = ""
        urls = ""

        while page.find("<p>") != -1:

            start = page.find("<p>") + 3
            end = page.find("</p>")

            words += page[start:end].split()

            page = page.replace("<p>", "", 1)
            page = page.replace("</p>", "", 1)

        while page.find("</a>") != -1:
            
            start = page.find('<a href="') + 9
            end = page.find('.html">') + 5

            urls += page[start:end] + " "

            page = page.replace('href="', "", 1)
            page = page.replace('.html">', "", 1)
            page = page.replace('</a>', "", 1)

        words = words.split()
        urls = urls.split()

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





print(webdev.read_url("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))  