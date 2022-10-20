import math
import os
import json
import crawler
import matmult

dict = json.load(open(os.path.join('crawl', "dict.json"), "r"))
reverseDict = json.load(open(os.path.join('crawl', "reverseDict.json"), "r"))

# returns a list of other URLs that the page with the given URL links to
def get_outgoing_links(url):

    # if the url wasn't found in the crawling process
    if url not in dict:
        return None

    list = []

    # retrieve the name of the folder of the specific url
    folderName = dict[url]    

    # find the path to the folder
    folderPath = os.path.join('crawl', folderName)

    # find the path to the url file
    urlFilePath = os.path.join(folderPath, "urls")

    # open file
    urls = open(urlFilePath, "r")

    for link in urls:
        # add every url to list
        list.append(link.strip())

    return list


# returns a list of URLs for pages that link to the page with the given URL
def get_incoming_links(url):

    # a list of urls for pages that link to the given url
    list = []

    # store the list of all folders in crawl
    folders = os.listdir("crawl")

    for folder in folders:
        # find the path to the url file
        urlFilePath = os.path.join(os.path.join("crawl", folder), "urls")

        # open the url folder
        urls = open(urlFilePath, "r")

        # check every link to see if it matches the given url
        for link in urls:
            if url == link.strip():
                # matched; add the url of this file's owner to list
                list.append(reverseDict[folder.split("_")[0]])
                break

    # if given url was not found during was not found
    if (len(list) == 0):
        return None

    return list


# omar
def get_page_rank(url):
    #Creating Adjacency  matrix
    adjacencyMat = []

    # outgoing_urls = [ n-0, n-3, n5  ]
    #print(reverseDict)

    #CREATING THE INITAL ADJACENCY MATRIX

    #TEST PURPOSES - GETTING THE MAP 

    # for k in range(len(dict)):

    #     themap = dict[reverseDict[k+1]]

    #     print(str(k) + " --> " + themap)

    # print()

    for i in range(len(reverseDict)):
        
        urlRow = []

        # print(reverseDict["1"])
        currUrl = reverseDict[str(i + 1)]

        links = get_outgoing_links(currUrl)

        # Adding the index maps for all the outgoing urls in the current row
        linkMaps = []
        for link in links:
            linkMaps.append(int(dict[link].split("_")[0]) - 1)
        linkMaps.sort()
        linkMaps.append("<end-map>")

        
        #going throught each column in the row
        for j in range(len(dict)):  

            #if the current column index and the link have the same map then adding 1 otherwise adding 0         
            if j == linkMaps[0]:
                urlRow.append(1)
                linkMaps.pop(0)
            else:
                urlRow.append(0)

        adjacencyMat.append(urlRow)
        #print(urlRow)

    # INTIAL PROBABILITY MATRIX

    #finding the sum of all values in a row
    rowSum = []
    for row in adjacencyMat:
        sum = 0
       
        for col in row:
            sum += col
        rowSum.append(sum)

    initialProbMat = []

    
    #Dividing each value in a row by the sum of values in it
    
    for i in range(len(adjacencyMat)):
        initialProbMat.append(matmult.mult_scalar([adjacencyMat[i]], 1/rowSum[i])[0])

    # print("\nTHIS IS THE INTIAL PROBABLITY MATRIX:")
    # for row in initialProbMat:
    #     print(row)

    #SCALEDED ADJACENCY MATRIX
    ALPHA = 0.1
    scaledMatrix = matmult.mult_scalar(initialProbMat, (1-ALPHA))

    # print("\nTHIS IS THE SCALED PROBABILITY MATRIX")
    # for row in scaledMatrix:
    #     print(row)

    #ADD ALPHA/N TO EACH ENTRY
    finalMatrix = []

    for row in scaledMatrix:
        finalRow = []
        for col in row:
            finalRow.append(col + (ALPHA/len(dict)))
        finalMatrix.append(finalRow)

    # print("\nTHIS IS THE FINAL MATRIX")
    # for row in finalMatrix:
    #     print(row)

    #POWER ITERATION
    initialValue = [[]]

    #sets the intial value as a row that has a sum of 1
    for i in range(len(dict)):
            initialValue[0].append(1/len(dict))

    #print(initialValue)
    
    prev = matmult.mult_matrix(initialValue, finalMatrix)
    curr = matmult.mult_matrix(prev, finalMatrix)
    ecDistance = matmult.euclidean_dist(prev, curr)

    while(ecDistance >  0.0001):

        prev = curr

        curr = matmult.mult_matrix(curr, finalMatrix)

        ecDistance = matmult.euclidean_dist(curr, prev)

        #print("Ec distance is: " + str(ecDistance))

    pageRanks = curr

    #print()
    #print(pageRanks)

    #print(int(dict[url].split("_")[0]) - 1)

    #WHAT IF THE PAGE DOESNT EXIST
    if url not in dict:
        return -1
    return pageRanks[0][int(dict[url].split("_")[0]) - 1]


#print(get_page_rank("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-3.html"))
#print(len(get_outgoing_links("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")))


# returns the inverse document frequency of that word within the crawled pages
def get_idf(word):

    # count of documents word appears in
    count = 0

    # store the list of all folders in crawl
    folders = os.listdir("crawl")

    for folder in folders:
        # check if they are folders (not json files)
        if os.path.isdir(os.path.join("crawl", folder)):
            # find the path to the word file
            wordFilePath = os.path.join(os.path.join("crawl", folder), "words")

            # open the url folder
            words = open(wordFilePath, "r")

            # check every link to see if it matches the given url
            for w in words:
                if word == w.strip():
                    # matched; increment count
                    count += 1
                    break

    # if given url was not found during was not found
    if (count == 0):
        return 0

    # math calculation breakdown
    count += 1
    temp = len(dict)/count
    return math.log(temp, 2)


# return the term frequency of that word within the page with the given URL
def get_tf(url, word):

    # if the url wasn't found in the crawling process
    if url not in dict:
        return 0

    # count of number of occurences of w in file
    wordCount = 0
    # count of total number of words
    totalCount = 0

    # retrieve the name of the folder of the specific url
    folderName = dict[url]
        

    # find the path to the folder
    folderPath = os.path.join('crawl', folderName)

    # find the path to the url file
    wordFilePath = os.path.join(folderPath, "words")

    # open file
    words = open(wordFilePath, "r")

    # for every word in the file check if it matches with the given word
    for w in words:
        if w.strip() == word:
            # matched; increment 
            wordCount += 1
        # increment total count of words in file
        totalCount += 1

    # if the given word does not appear in the page 
    if (wordCount == 0):
        return 0

    return wordCount/totalCount
    

# return the tf-idf weight for the given word within the page represented by the given URL
def get_tf_idf(url, word):
    return math.log(1+get_tf(url, word), 2)*get_idf(word)


'''
# test cases:
crawler.crawl('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html')

# 2 3 4 5 6 7 8 9
s0 = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"
# 1  
s1 = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-1.html"
# 1 9 10
s8 = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-8.html"

# print(get_outgoing_links(s0))

# # total kiwi : 7
# print(get_idf("kiwi"))

# # s0, coconut = 3/23
# print(get_tf(s0, "none"))

# # kiwi; idf: log(10/1+7) tf: 2/23
# print(get_tf_idf(s0, "kiwi"))

'''


