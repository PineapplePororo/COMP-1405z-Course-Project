from crawler import dict, reverseDict
import matmult
import math
import os


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


# alvina
def get_incoming_links(url):

    # a lsit of urls for pages that link to the given url
    list = []

    # store the list of all folders in crawl
    folders = os.listdir("crawl")

    for folder in folders:
        # find the path to the url file
        urlFilePath = os.path.join(os.path.join("crawl", folder), "urls")

        urls = open(urlFilePath, "r")

        # for link in urls:
        #     if link == url:


    '''
    returns a list of URLs for pages that link to the page with the given URL
    
    - folders = os.listdir("crawl")
    - for folder in folders:
        os.path.join(folder, "url")

        go through each line check if url is in the file

    '''
    pass

# omar
def get_page_rank(url):

    '''
    returns the pagerank value of the page with that url

    watch lecture video
    alpha value of 0.1
    Euclidean distance
    
    '''
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

        currUrl = reverseDict[i + 1]

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

# omar
def get_idf(word):
    
    '''
    returns the inverse document frequency of that word within the crawled pages

    change crawler.py 
    - have dict key: word value: # of doucuments words appear in

    total number of documents - len(dict)
    '''
    pass

# omar
def get_tf(url, word):

    '''
    return the term frequency of that word within the page with the given URL
    '''

    pass

# alvina
def get_tf_idf(url, word):

    '''
    return the tf-idf weight for the given word within the page represented by the given URL

    '''
    pass


s = "http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"

print(get_incoming_links(s))