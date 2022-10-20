import webdev
import os

# key: url , value:full folder name
dict = {}
# key: the number before the underscore in folder name , key: url
reverseDict = {}

# checks if the main folder that will have all the folders from crawl is made and empty
# void method
def manageFolder():
    # create a folder that will contain all the folders from the crawl
    if os.path.exists("crawl"):
        # if it's created already, check if there are files in the folder

        # create a list of folders/files in the crawl folder
        dirs = os.listdir("crawl")

        # loop for all the subfolders in the crawl folder
        for dir in dirs:
            # store the path of the subfolder
            subfolderPath = os.path.join("crawl", dir)

            # make a list of all files in the subfolder
            files = os.listdir(subfolderPath)

            # loop for all the files in subfolder
            for file in files:
                # remove every file
                os.remove(os.path.join(subfolderPath, file))
            # remove the subfolder
            os.rmdir(subfolderPath)
    else:
        # if there isn't, make a new folder 
        os.makedirs("crawl")


# fuction to create the necessary folder and files
# returns the word file path and url file path so that it could be used in crawl(seed)
def createFiles(currentFile):

    # store path for the subfolder of the current file
    filePath = os.path.join('crawl', currentFile)

    # create a directory for the url
    # check if the folder with the same name exists
    if os.path.exists(filePath):
        print("currentFile exists in crawl")
    else:
        # if there isn't, make a new folder with a name same as the url
        os.makedirs(filePath)

    # create files within the created folder
    if os.path.isdir(filePath):
        # create two files: words for storing words and url for storing urls
        wordPath = os.path.join(filePath, "words")
        urlPath = os.path.join(filePath, "urls")

        # create an empty word file
        if not os.path.exists(wordPath):
            open(wordPath, "w").close()

        # create an empty url file
        if not os.path.exists(urlPath):
            open(urlPath, "w").close()

    return wordPath, urlPath

def crawl(seed):

    global dict, reverseDict

    # keeps track of the pages visited (used for runtime efficiency)
    # it has a url of seed at first
    dict = {seed:1}
    # keeps track of urls that have been yet to be parsed through
    # it has a url of seed at first
    queue = [seed]
    # keeps track of the number of total pages found & folder name of the specific url
    count = 1

    # check if the main folder that will store all the information is made and empty
    manageFolder()

    while (len(queue) > 0):

        # get the next url to parse through
        url = queue.pop()

        #finding the abosolute url by finding the last "/" and saving its index
        lastSlash = 0
        for i in range(len(url) - 1, -1, -1):

            if(url[i] == "/"):
                lastSlash = i
                break

        #saving the absolute url by makign it a substring of the current url from its start until the last "/"
        absoluteUrl = url[0:lastSlash]

        # retrieve title 
        title = url[lastSlash + 1:]

        # add to reverse dict
        reverseDict[dict[url]] = url

        # since value of a key is the title of the folder, add the title to the folder name
        dict[url] = str(dict[url]) + "_" + title
        # create folder and files for the url
        wordFile, urlFile = createFiles(str(dict[url]))


        page = webdev.read_url(url)
        
        words = ""
        urls = ""

        while page.find("<p>") != -1:

            start = page.find("<p>") + 3
            end = page.find("</p>")

            words += page[start:end]

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

        fileOut = open(wordFile, "w")

        for word in words:
            fileOut.write(word + "\n")
        
        fileOut.close()

        fileOut = open(urlFile, "w")

        for url in urls:
            if(url[0] == "."):
                url = absoluteUrl + url[1:len(url)]
            
            fileOut.write(url + "\n")

            # adding to queue 
            # check if the url isn't in queue 
            if url not in dict:
            
                # increment count for all succeed crawls
                count += 1

                # make a new key of the url
                dict[url] = count

                # add to end of queue
                queue.append(url)
        

    return count 


# crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")

# def time():
#     import time
#     start = time.time()
#     crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")
#     end = time.time()
#     print(end - start)

# time()