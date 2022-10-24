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
    # for pagerank 
    open(os.path.join('crawl', "0_pageRank.json"), "w").close()
    
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

    # Creating a queue to contain all urls to crawl through
    queue = [seed]
    count = 1

    # Getting the seed's title
    for i in range(len(seed) - 1, -1, -1):
            if(seed[i] == "/"):
                lastSlash = i
                break
    
    # retrieve title 
    title = seed[lastSlash + 1:].split(".")[0]

    # Creating a dictionary to map all urls to a number {url: number + title}
    dict = {seed: "1_" + title}

    # Creating reverse dictionary to map all number to a url {number: url }
    reverseDict = {1:seed}

    manageFolder()

    twf = {}
    tf = {}
    incoming = {}

    while(len(queue) >  0):  
        currUrl = queue.pop()

        urlFile = createFiles(dict[currUrl])

        page = webdev.read_url(currUrl)

        words = ""
        urls = ""

        # Extracting all urls form the curretn url's page
        while page.find("</a>") != -1:
            
            #Finding the starting portion of the a-tag and the ending portion of the link
            #Using those values to extract the link itself
            start = page.find('<a href="') + 9
            end = page.find('.html">') + 5

            urls += page[start:end] + " "

            #Replacing the tags to prevent it form being read again
            page = page.replace('href="', "", 1)
            page = page.replace('.html">', "", 1)
            page = page.replace('</a>', "", 1)

        urls = urls.split()

        #finding the abosolute url by finding the last "/" and saving its index
        lastSlash = 0
        for i in range(len(currUrl) - 1, -1, -1):

            if(currUrl[i] == "/"):
                lastSlash = i
                break

       #saving the absolute url by makign it a substring of the current url from its start until the last "/"
        absoluteUrl = currUrl[0:lastSlash]

        # Writing the urls to a file
        fileOut = open(urlFile, "w")

        for url in urls:
            if(url[0] == "."):
                url = absoluteUrl + url[1:]
            
            fileOut.write(url + "\n")

            if url not in dict:
                
                #incrementing count
                count += 1

                #getting the url's title
                title = ""  

                #getting the last slash of the current url
                for i in range(len(url) - 1, -1, -1):
                    if(url[i] == "/"):
                        lastSlash = i
                        break
                
                # retrieve title 
                title = url[lastSlash + 1:].split(".")[0]

                #Adding the url to dict
                dict[url] = str(count) + "_" + title

                #Adding url to reverseDict
                reverseDict[count] = url

                #appending the url onto the queue
                queue.append(url)
        
        fileOut.close()

        # Extracting all words by finding the start and end p-tags and splicing the strings using those
        while page.find("<p>") != -1:

            start = page.find("<p>") + 3
            end = page.find("</p>")

            words += page[start:end]

            page = page.replace("<p>", "", 1)
            page = page.replace("</p>", "", 1)

        words = words.split()
        
        uniqueWords = {}

        # Getting the count for each word in the url and storing as a variable
        for word in words:
            if word in uniqueWords:
                uniqueWords[word] += 1
            else:
                uniqueWords[word] = 1
            
        #Getting the frequency of each word and storing it in the uniquewords dictionary
        for word in uniqueWords:
            uniqueWords[word] = uniqueWords[word]/len(words)
            
            if word in twf:
                twf[word] += 1
            else:
                twf[word] = 1

        # Adding the uniqueWrods to tf
        tf[dict[currUrl].split("_")[0]] = uniqueWords

        #Incoming links
        for url in urls:
            
            urlNum = dict[(absoluteUrl + url[1:])].split("_")[0]

            #If the url is already in the incoming dictionary adding the url to the list
            if urlNum in incoming:
                # Appending the url into a list inside the dictionary
                incoming[urlNum].append(currUrl)
            else:
                incoming[urlNum] = []
                incoming[urlNum].append(currUrl)

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


# crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")

# def time():
#     import time
#     start = time.time()
#     print(crawl('http://people.scs.carleton.ca/~davidmckenney/fruits/N-0.html'))
#     search.search('peach apple apple apple banana peach peach banana',True)
#     end = time.time()
#     print(end - start)

# time()