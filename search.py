import searchdata
import json
import os

dict = json.load(open(os.path.join('crawl', "0_dict.json"), "r"))
reverseDict = json.load(open(os.path.join('crawl', "0_reverseDict.json"), "r"))

def search(phrase, boost):
   
    query = []
    docVector = []

    '''
    - split phrase into list - query
    - tf-idf of query
    - tf-idf of documents for all elements

    - cosine similarity
    - boost is true, call pageRank and mulitply similarity with pageRank
    - sort

    - top 10 documents of cosine similarity 
    '''

    # COSINE SIMILARITY CODE

    cosSimilarity = []

    # Finding the cosine similarity for each document
    for i in len(docVector):
        
        # A dictionary which will store url, title and score
        cosDict = {}

        numerator = 0

        #Finding the denominator
        for j in range(len(query)):
            numerator += query[j]  + docVector[i][j]
    
        # Finding the left denominator sqrt(sumof[q**2])
        leftDenom = 0
        for j in range(len(query)):
            leftDenom += query[j]**2
        
        leftDenom = leftDenom**0.5

        # Finding the right denominator sqrt(sumof[q**2])
        rightDenom = 0
        for j in range(len(docVector[i])):
            rightDenom += docVector[i][j]**2
        
        rightDenom = rightDenom**0.5

        # Getting the url of the cosSimilarity
        url = searchdata.reverseDict[i+1]

        # Adding to the dictionary
        cosDict["url"] = url
        cosDict["title"] = dict[url].split("_")[1]
        cosDict["score"] =  numerator/(leftDenom*rightDenom)
        
        # Finding and appending the cosine similarity to the cosSimilarity list
        cosSimilarity.append(cosDict)

    # BOOST CODE

    # If there is boost then multiplying the cosine similarity (otherwise leaving it the same)
    if(boost):
        for i in range(cosSimilarity):
            cosSimilarity[i]['score'] *= searchdata.get_page_rank(cosSimilarity[i]["url"])

    # TOP 10 DOCUMENTS

    topSimilarity = []

    for i in range(10):
        topSimilarity.append(cosSimilarity[i])

    for i in range(11, len(cosSimilarity)):
        
        #Add next element to the topSimilarity
        topSimilarity.append(cosSimilarity[i])
        
        #Sort topSimilarity (using bubble sort technique)
        for j in range(1, len(cosSimilarity)):
            for k in range(i, cosSimilarity):

                curr = cosSimilarity[k]
                prev = cosSimilarity[k-1]

                currVal = curr["score"]
                prevVal = prev["score"]

                if(prevVal < currVal):
                    temp = curr
                    curr = prev
                    prev = temp

        #Remove the last element
        topSimilarity.pop()

    #BUBBLE SORT OR SMTHN
    # for i in range(1, len(cosSimilarity)):
    #     for j in range(i, cosSimilarity):

    #         curr = cosSimilarity[j]
    #         prev = cosSimilarity[j-1]

    #         currVal = curr[1]
    #         prevVal = prev[1]

    #         if(prevVal < currVal):
    #             temp = curr
    #             curr = prev
    #             prev = temp
    



