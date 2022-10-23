import searchdata
import json
import os
import math
import crawler

dict = json.load(open(os.path.join('crawl', "0_dict.json"), "r"))
reverseDict = json.load(open(os.path.join('crawl', "0_reverseDict.json"), "r"))


# return a list of the top 10 ranked search results
def search(phrase, boost):

    # store words in a list
    words = phrase.split(" ")

    # contains tf-idf values for all documents 
    docVector = []
    
    # for all documents
    for i in range(len(reverseDict)):
        # temporary storage of tfidf values of a document
        row = []
        # for words in phrase
        for j in words:
            # store the tfidf of the word 
            row.append(searchdata.get_tf_idf(reverseDict[str(i+1)], j))
        # add row 
        docVector.append(row)
    
    # list that stores tf-idf value of words inputted
    query = []

    # value of tf for phrase
    tf = 1/len(words)

    for i in range(len(words)):
        # tf-idf value for query
        query.append(math.log(1+tf, 2)*searchdata.get_idf(words[i]))
    
    # COSINE SIMILARITY CODE

    print(docVector)
    print()
    print(query)

    cosSimilarity = []

    leftDenom = 0
     # Finding the left denominator sqrt(sumof[q**2])
        
    for j in range(len(query)):
        leftDenom += query[j]**2
    
    leftDenom = leftDenom**0.5

    # Finding the cosine similarity for each document
    for i in range(len(docVector)):
        
        # A dictionary which will store url, title and score
        cosDict = {}

        numerator = 0
        #Finding the numerator
        for j in range(len(query)):
            numerator += query[j]  + docVector[i][j]
    
      
        # Finding the right denominator sqrt(sumof[q**2])
        rightDenom = 0
        for j in range(len(docVector[i])):
            rightDenom += docVector[i][j]**2
        
        rightDenom = rightDenom**0.5

        # Getting the url of the cosSimilarity
        url = searchdata.reverseDict[str(i+1)]
        # Adding to the dictionary
        cosDict["url"] = url
        cosDict["title"] = dict[url].split("_")[1]

        if(numerator == 0 or leftDenom == 0 or rightDenom == 0):
            cosDict["score"] = 0
        else:
            cosDict["score"] =  numerator/(leftDenom*rightDenom)
        
        # Finding and appending the cosine similarity to the cosSimilarity list
        cosSimilarity.append(cosDict)

    # BOOST CODE

    # If there is boost then multiplying the cosine similarity (otherwise leaving it the same)
    if(boost):
        for i in range(len(cosSimilarity)):
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

    return topSimilarity

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
    
crawler.crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")

search("kiwi banana peach", False)