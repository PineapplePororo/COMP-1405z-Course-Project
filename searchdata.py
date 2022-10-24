import math
import os
import json
import matmult

dict = json.load(open(os.path.join('crawl', "0_dict.json"), "r"))
reverseDict = json.load(open(os.path.join('crawl', "0_reverseDict.json"), "r"))
incoming = json.load(open(os.path.join('crawl', "0_incoming.json"), "r"))
twf = json.load(open(os.path.join('crawl', "0_twf.json"), "r"))
tf = json.load(open(os.path.join('crawl', "0_tf.json"), "r"))

# returns a list of other URLs that the page with the given URL links to
def get_outgoing_links(url):

    # if the url wasn't found in the crawling process
    if url not in dict:
        return None

    list = []

    # retrieve the name of the folder of the specific url
    folderName = dict[url]    

    # find the path to the file
    urlFilePath = os.path.join('crawl', folderName)

    # open file
    urls = open(urlFilePath, "r")

    for link in urls:
        # add every url to list
        list.append(link.strip())

    return list


# returns a list of URLs for pages that link to the page with the given URL
def get_incoming_links(url):

    # if url was not found during the crawl process
    if url not in dict:
        return None

    numberUrl = dict[url].split("_")[0]

    # if there is no incoming links to url
    if numberUrl not in incoming:
        return None

    return incoming[numberUrl]


# returns the PageRank value of the page with that URL
def get_page_rank(url):

    # url not found during the crawling process
    if url not in dict:
        return -1

    # if the list has already been created
    if os.path.getsize(os.path.join('crawl', "0_pageRank.json")) != 0:
        # open file
        pageRank = json.load(open(os.path.join('crawl', "0_pageRank.json"), "r"))
        # return the corresponding pagerank value of url
        return pageRank[0][int(dict[url].split("_")[0]) - 1]
    else:
        # creating an empty adjacency  matrix
        adjacencyMat = []

        # finishing adjacency matrix
        for i in range(len(reverseDict)):

            # intializing row
            row = [0.0]*len(reverseDict)

            # grab all the links that is linked to the current index of the matrix
            links = get_outgoing_links(reverseDict[str(i + 1)])

            # if there is no outgoing links
            if len(links) == 0:
                # for every entry 
                for col in range(len(reverseDict)):
                    # adjacency = have value be 1/N 
                    # then (1-alpha * adjacency) for scaled adjacency matrix
                    # final adjcency matrix: add alpha/N
                    row[col] = ((1/len(reverseDict))*(1-0.1)) + (0.1/len(reverseDict))
            # if there are outgoing links
            else:
                # for all links linked
                for link in links:
                    # adjacency = find the corresponding column index of the link and set it to 1
                    # then (1-alpha * adjacency) for scaled adjacency matrix
                    row[int(dict[link].split("_")[0])-1] = (1/len(links))*(1-0.1)
                # for every entry 
                for col in range(len(reverseDict)):
                    # final adjcency matrix: add alpha/N
                    row[col] = row[col] + (0.1/len(reverseDict))

            # inserting row to end of adjacency matrix
            adjacencyMat.insert(i, row)

        
        # POWER ITERATION
        initialValue = [adjacencyMat[0]]
        
        # find matrix of prev, curr and calculate Euclidean distance
        prev = matmult.mult_matrix(initialValue, adjacencyMat)
        curr = matmult.mult_matrix(prev, adjacencyMat)
        ecDistance = matmult.euclidean_dist(prev, curr)

        # loop ends when Euclidean distance is below 0.0001
        while(ecDistance >  0.0001):

            prev = curr

            # multiply the matrixes
            curr = matmult.mult_matrix(curr, adjacencyMat)
            # recalculate Euclidean distance
            ecDistance = matmult.euclidean_dist(curr, prev)

        # store output to json 
        with open(os.path.join('crawl', "0_pageRank.json"), 'w') as outfile:
            json.dump(curr, outfile, indent=4, ensure_ascii=False)

        # return the corresponding pagerank value of url
        return curr[0][int(dict[url].split("_")[0]) - 1]


# returns the inverse document frequency of that word within the crawled pages
def get_idf(word):

    # if word wasn't found during the crawl process
    if word not in twf:
        return 0

    # calculation
    temp = len(dict)/(1+twf[word])
    return math.log(temp, 2)


# return the term frequency of that word within the page with the given URL
def get_tf(url, word):

    # if url was not found during the crawl process
    if url not in dict:
        return 0

    key = dict[url].split("_")[0]

    # if the url wasn't found in the crawling process
    if key not in tf:
        return 0

    # if the given word does not appear in the page 
    if (word not in tf[key]):
        return 0

    return tf[key][word]
    

# return the tf-idf weight for the given word within the page represented by the given URL
def get_tf_idf(url, word):

    # calculate idf
    idf = get_idf(word)

    # if idf is zero, answer will always be zero
    if (idf == 0):
        return 0

    # calculation tf-idf value
    return math.log(1+get_tf(url, word), 2)*idf


