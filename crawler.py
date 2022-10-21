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

    #total word frequency
    twf = {}
    tf = {}
    incoming = {}

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

        uniqueWords = {}

        # Extracting all words by finding the start and end p-tags and splicing the strings using those
        while page.find("<p>") != -1:

            start = page.find("<p>") + 3
            end = page.find("</p>")

            words += page[start:end]

            page = page.replace("<p>", "", 1)
            page = page.replace("</p>", "", 1)

        words = words.split()

        # Getting the count for each word in the url and storing as a variable
        for word in words:
            if word in twf:
                twf[word] += 1
            else:
                twf[word] = 0

            if word in tf:
                uniqueWords[word] += 1
            else:
                uniqueWords[word] = 1
        
        #Getting the frequency of each word and storing it in the uniquewords dictionary
        for word in uniqueWords:
            uniqueWords[word] /= len(words) 
        
          #Adding the uniques wrods of the current url into the tf dictionary
        tf[dict[url].split("_")[0]] = uniqueWords

        # Extracting links by finding the starting portion of the a-tag and the end of the link and using those indexes to splice
        while page.find("</a>") != -1:
            
            start = page.find('<a href="') + 9
            end = page.find('.html">') + 5

            urls += page[start:end] + " "

            page = page.replace('href="', "", 1)
            page = page.replace('.html">', "", 1)
            page = page.replace('</a>', "", 1)

        urls = urls.split()          


        #Writing all the urls to the url files
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

        #THIS IS THE CODE FOR INCOMING
        # Getting incoming links for all links in teh crawl
        for link in urls:
            if(link in incoming):
                #appending the url into a list (value) inside the incoming dictionary
                incoming[dict[str(absoluteUrl + link[1:])].split("_")[0]].append(url)
            else:
                #if the incoming list does not already exist, creating it then appending the url into it
                incoming[dict[str(absoluteUrl + link[1:])].split("_")[0]] = []
                incoming[dict[str(absoluteUrl + link[1:])].split("_")[0]].append(url)  

    print("\n\n")
    print(twf)
    print("\n\n")
    print(tf)
    print("\n\n")
    print(incoming)

    # dump to all dictioinaries to files using json
    with open(os.path.join('crawl', "0_dict.json"), 'w') as outfile:
        json.dump(dict, outfile, indent=4, ensure_ascii=False)
        
    with open(os.path.join('crawl', "0_reverseDict.json"), 'w') as outfile:
        json.dump(reverseDict, outfile, indent=4, ensure_ascii=False)

    with open(os.path.join('crawl', "0_incoming.json"), 'w') as outfile:
        json.dump(incoming, outfile, indent=4, ensure_ascii=False)
    
    with open(os.path.join('crawl', "0_twf.json"), 'w') as outfile:
        json.dump(twf, outfile, indent=4, ensure_ascii=False)
    
    with open(os.path.join('crawl', "0_tf.json"), 'w') as outfile:
        json.dump(tf, outfile, indent=4, ensure_ascii=False)
    
    return count 


crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")

# def time():
#     import time
#     start = time.time()
#     crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")
#     end = time.time()
#     print(end - start)

# time()