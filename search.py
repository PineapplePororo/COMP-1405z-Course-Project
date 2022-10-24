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

    total = len(words)

    # print("words before: ")
    # print(words)

    sameWord = {}

    for word in words:
        if word not in sameWord:
            sameWord[word] = 1
        else:
            sameWord[word] += 1

    words = []

    for word in sameWord:
        words.append(word)
    
    # print("words after: ")
    # print(words)

    # contains tf-idf values for all documents 
    docVector = []
    
    # idf print
    # for word in words:
    #     print(word + ": " + str(searchdata.get_idf(word)))

    # for all documents
    for i in range(len(reverseDict)):
        # temporary storage of tfidf values of a document
        row = []
        # for words in phrase
        for j in words:
            # print(reverseDict[str(i+1)])
            # print("j: " + j)
            # store the tfidf of the word 
            row.append(searchdata.get_tf_idf(reverseDict[str(i+1)], j))
            # print("tf-idf: " + str(searchdata.get_tf_idf(reverseDict[str(i+1)], j)))
        # add row 
        docVector.append(row)
    
    # list that stores tf-idf value of words inputted
    query = []

    for i in range(len(words)):
        # tf-idf value for query
        query.append(math.log(1+((sameWord[words[i]])/total), 2)*searchdata.get_idf(words[i]))
    
    # for line in docVector:
    #     print(line)
    # print()
    # print(query)

    # COSINE SIMILARITY CODE

    cosSimilarity = []

    leftDenom = 0
    # Finding the left denominator sqrt(sumof[q**2])
        
    # left denominator calculation (same throughout the calculation)
    for j in range(len(query)):
        leftDenom += query[j]**2
    leftDenom = leftDenom**0.5

    # Finding the cosine similarity for each document
    for i in range(len(docVector)):
        
        # A dictionary which will store url, title and score
        cosDict = {}

        # finding the numerator
        numerator = 0
        for j in range(len(query)):
            numerator += query[j]*docVector[i][j]
      
        # Finding the right denominator
        rightDenom = 0
        for j in range(len(query)):
            rightDenom += docVector[i][j]**2
        rightDenom = rightDenom**0.5

        # Getting the url of the cosSimilarity
        url = searchdata.reverseDict[str(i+1)]
        # Adding to the dictionary
        cosDict["url"] = url
        # addint title to the dictionary 
        cosDict["title"] = dict[url].split("_")[1]
        # print(cosDict["title"])

        # if any of the num or den is zero
        if(numerator == 0 or leftDenom == 0 or rightDenom == 0):
            # score is zero
            cosDict["score"] = 0
        else:
            # print("numerator: " + str(numerator))
            # print("leftDenom: " + str(leftDenom))
            # print("rightDenom: " + str(rightDenom))
            # print("(numerator/(leftDenom*rightDenom)): " + str((numerator/(leftDenom*rightDenom))))
            if(boost):
                # if there is boost, multiply cosine similarity with page rank
                cosDict["score"] =  searchdata.get_page_rank(url) * (numerator/(leftDenom*rightDenom))
            else:
                # no boost; just store score
                cosDict["score"] = numerator/(leftDenom*rightDenom)
            
        # print("score: " + str(cosDict["score"]))

        if(len(cosSimilarity) < 10):
            # print("filling")
            cosSimilarity.append(cosDict)

            if (len(cosSimilarity) == 10):
                # print("firstTen")
                #Sort cosSimilarity (bubble sort technique)
                for j in range(len(cosSimilarity)):
                    # last element is already in place
                    for k in range(len(cosSimilarity)-j-1):
                        # if current score is smaller than k+1 score
                        if (cosSimilarity[k]["score"] < cosSimilarity[k+1]["score"]):
                            # switch places
                            temp = cosSimilarity[k]
                            cosSimilarity[k] = cosSimilarity[k+1]
                            cosSimilarity[k+1] = temp
        # if the last index's score of cosSimilarity is smaller than score just retrieved
        elif(cosSimilarity[9]["score"] < cosDict["score"]):
            # print("last index small")
            # remove the last index
            cosSimilarity.pop()

            # append the element that was just created to cosSimilarity at the right place
            for k in range(len(cosSimilarity)):
                # if score that is being added is greater than current k score
                if (cosSimilarity[k]["score"] < cosDict["score"]):
                    # insert current score 
                    cosSimilarity.insert(k, cosDict)
                    break
            
            if (len(cosSimilarity) < 10):
                cosSimilarity.append(cosDict)
        
        # print("===========================")
        # for line in cosSimilarity:
        #     print(line)
        

    return cosSimilarity

# crawler.crawl('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html')

# search('coconut coconut orange blueberry lime lime lime tomato',False)