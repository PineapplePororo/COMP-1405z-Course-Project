import abc
import webdev
import os

def crawl(seed):
    # keeps track of the pages visited (used for runtime efficiency)
    dict = {}
    # 
    queue = []
    # keeps track of the number of total pages found
    count = 0

    url = seed 

    while (len(queue) != 0):

        currentFile = abc
        
        # create folder and files for the url
        wordFile, urlFile = createFolderFiles(currentFile)

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


# fuction to create the necessary folder and files
def createFolderFiles(currentFile):

    # if os.path.exists("crawl"):
    #     print("folder exists")
    # else:
    #     # if there isn't, make a new folder with a name as the url
    #     os.makedirs("crawl")

    # create a directory for the url
    # check if the folder with the same name exists
    if os.path.exists(currentFile):
        print("folder exists")
    else:
        # if there isn't, make a new folder with a name as the url
        os.makedirs(currentFile)

    # create files within the created folder
    if os.path.isdir(currentFile):
        # create two files: words for storing words and url for storing urls
        wordPath = os.path.join(currentFile, "words")
        urlPath = os.path.join(currentFile, "urls")

    return wordPath, urlPath



    

    



# print(webdev.read_url("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))


