import webdev
import os

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

    # check for any #\/:*?"<>|" and replace them with spaces as they aren't allowed to be in a folder
    currentFile = currentFile.replace("\\", " ").replace('/', " ").replace(':', " ").replace('*', " ").replace('?', " ").replace('\"', " ").replace('<', " ").replace('>', " ").replace('|', " ")

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

    # keeps track of the pages visited (used for runtime efficiency)
    dict = {}
    # keeps track of urls that have been yet to be parsed through
    queue = [seed]
    # keeps track of the number of total pages found
    count = 0

    # check if the main folder that will store all the information is made and empty
    manageFolder()

    while (len(queue) != 0):

        url = queue.pop()

        #finding the abosolute url by finding the last "/" and saving its index
        end = 0
        for i in range(len(url) - 1, -1, -1):

            if(url[i] == "/"):
                end = i
                break
        
        #saving the absolute url by makign it a substring of the current url from its start until the last "/"
        absoluteUrl = url[0:end]

        # create folder and files for the url
        wordFile, urlFile = createFiles(url[7:])
        # page = webdev.read_url(url)
        
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

        fileOut = open(wordFile, "r")

        for word in words:
            fileOut.write(word)
        
        fileOut.close()

        fileOut = open(urlFile, "r")

        for url in urls:
            if(url[0] == "."):
                fileOut.write(absoluteUrl + url[1:len(url) - 1])
            else:
                fileOut.write(url)
                

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

print(crawl("https://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))  