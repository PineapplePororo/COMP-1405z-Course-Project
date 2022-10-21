import webdev
import os
import json

# checks if the main folder that will have all the folders from crawl is made and empty
# void method
def manageFolder():
    # create a folder that will contain all the files from the crawl
    if os.path.exists("crawl"):
        # if it's created already, check if there are files in the folder

        # create a list of files in the crawl folder
        files = os.listdir("crawl")

        # loop for all files in crawl
        for file in files:
            # remove every file
            os.remove(os.path.join("crawl", file))
    else:
        # if there isn't, make a new folder 
        os.makedirs("crawl")

    # creating necessary json files
    open(os.path.join('crawl', "0_dict.json"), "w").close()
    open(os.path.join('crawl', "0_reverseDict.json"), "w").close()
    open(os.path.join('crawl', "0_incoming.json"), "w").close()
    open(os.path.join('crawl', "0_twf.json"), "w").close()
    open(os.path.join('crawl', "0_tf.json"), "w").close()
    

# fuction to create the necessary folder and files
# returns the word file path and url file path so that it could be used in crawl(seed)
def createFiles(currentFile):

    # store path for the subfolder of the current file
    filePath = os.path.join('crawl', currentFile)

    # create an empty word file
    if not os.path.exists(filePath):
        open(filePath, "w").close()

    return filePath

def crawl(seed):

    # key: the number before the underscore in folder name , key: url
    reverseDict = {}

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
        urlFile = createFiles(str(dict[url]))


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

        fileOut.close()
        

    # dump to file using json
    with open(os.path.join('crawl', "dict.json"), 'w') as outfile:
        json.dump(dict, outfile, indent=4, ensure_ascii=False)

    with open(os.path.join('crawl', "reverseDict.json"), 'w') as outfile:
        json.dump(reverseDict, outfile, indent=4, ensure_ascii=False)

    return count 


# crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")

# def time():
#     import time
#     start = time.time()
#     crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")
#     end = time.time()
#     print(end - start)

# time()