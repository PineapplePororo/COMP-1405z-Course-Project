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
def createFiles(fileName):

    # check for any #\/:*?"<>|" and replace them with spaces as they aren't allowed to be in a folder
    #currentFile = currentFile.replace("\\", " ").replace('/', " ").replace(':', " ").replace('*', " ").replace('?', " ").replace('\"', " ").replace('<', " ").replace('>', " ").replace('|', " ")

    # store path for the subfolder of the current file
    wordFilePath = os.path.join('crawl', "words")
    urlFilePath = os.path.join('crawl', "urls")

    # create a directory for the url
    # check if the folder with the same name exists
    if os.path.exists(wordFilePath):
        pass
        #print("currentFile exists in crawl")
    else:
        # if there isn't, make a new folder with a name same as the url
        os.makedirs(wordFilePath)
    
    # create a directory for the url
    # check if the folder with the same name exists
    if os.path.exists(urlFilePath):
        print("currentFile exists in crawl")
    else:
        # if there isn't, make a new folder with a name same as the url
        os.makedirs(urlFilePath)

    # create files within the created folder
    if os.path.isdir(wordFilePath):
        # create two files: words for storing words and url for storing urls
        wordPath = os.path.join(wordFilePath, fileName)
        urlPath = os.path.join(wordFilePath, fileName)

        # create an empty word file
        if not os.path.exists(wordPath):
            open(wordPath, "w").close()

    # create files within the created folder
    if os.path.isdir(urlFilePath):
        # create two files: words for storing words and url for storing urls
        wordPath = os.path.join(urlFilePath, fileName)
        urlPath = os.path.join(urlFilePath, fileName)

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

    counter = 1
    while (len(queue) != 0):

        #print(counter) 
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
        if(url not in dict): # creating the file if it has not yet been looked at
            wordFile, urlFile = createFiles(str(counter))
            counter += 1

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
            fileOut.write(word  +"\n")
        
        fileOut.close()

        fileOut = open(urlFile, "w")

        for url in urls:
            if(url[0] == "."):
                fileOut.write(absoluteUrl + url[1:len(url)])
                 # adding to queue 
                # check if the url isn't in queue 
                if url not in dict:
                
                    # make a new key of the url
                    dict[url] = 0

                    # add to end of queue
                    queue.append(absoluteUrl + url[1:len(url)])

                    # increment count for all succeed crawls
                    count += 1
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

print("THE COUNT IS: "  + crawl("https://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))  