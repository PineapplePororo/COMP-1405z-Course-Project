import abc
import webdev
import os

def crawl(seed):
    # keeps track of the pages visited (used for runtime efficiency)
    dict = {}
    # keeps track of urls that have been yet to be parsed through
    queue = []
    # keeps track of the number of total pages found
    count = 0

    # check if the main folder that will store all the information is made and empty
    manageFolder()

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

# checks if the main folder that will have all the folders from crawl is made and empty
# void method
def manageFolder():
    # create a folder that will contain all the folders from the crawl
    if os.path.exists("crawl"):
        # if it's created already, check if there are files in the folder
        dirs = os.listdir("crawl")

        # loop for all the subfolders in the crawl folder
        for dir in dirs:
            # loop for all the files in subfolder
            for file in dir:
                # remove every file
                os.remove(os.path.join(dir, file))
            # remove the subfolder
            os.rmdir(dir)
    else:
        # if there isn't, make a new folder 
        os.makedirs("crawl")


# fuction to create the necessary folder and files
# returns the word file path and url file path so that it could be used in crawl(seed)
def createFolderFiles(currentFile):

    # create a directory for the url
    # check if the folder with the same name exists
    if os.path.exists(os.path.join('crawl', currentFile)):
        print("currentFile exists in crawl")
    else:
        # if there isn't, make a new folder with a name same as the url
        os.makedirs(os.path.join('crawl', currentFile))

    # create files within the created folder
    if os.path.isdir(os.path.join('crawl', currentFile)):
        # create two files: words for storing words and url for storing urls
        wordPath = os.path.join(currentFile, "words")
        urlPath = os.path.join(currentFile, "urls")

    return wordPath, urlPath



# print(webdev.read_url("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))


