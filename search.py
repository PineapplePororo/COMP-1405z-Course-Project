import searchdata
import json
import os
import math
import crawler

dict = json.load(open(os.path.join('crawl', "0_dict.json"), "r"))
reverseDict = json.load(open(os.path.join('crawl', "0_reverseDict.json"), "r"))


# return a list of the top 10 ranked search results
def search(phrase, boost):

    # # print("PHRASE: ")
    # # print(phrase)


    # # store words in a list
    # words = phrase.split(" ")

    # # contains tf-idf values for all documents 
    # docVector = []
    

    # uniqueWords = {}

    # for word in words:
    #     if(word not in docVector):
    #         uniqueWords[word] = 1
    #     else:
    #         uniqueWords[word] += 1
    
    # for i in range(len(reverseDict)):
        
    #     vector = []

    #     for word in uniqueWords:

    #         vector.append(searchdata.get_tf_idf(reverseDict[str(i+1)], word))

    #     docVector.append(vector)

    # # # for all documents
    # # for i in range(len(reverseDict)):
    # #     # temporary storage of tfidf values of a document
    # #     row = []
    # #     # for words in phrase
    # #     for j in words:
    # #         # store the tfidf of the word 
    # #         row.append(searchdata.get_tf_idf(reverseDict[str(i+1)], j))
    # #     # add row 
    # #     docVector.append(row)
    
    # # list that stores tf-idf value of words inputted

    # # # value of tf for phrase
    # # tf = 1/len(words)9
    
    # # QUERY CODE
    # query = []
    # sameWord = {}

    # for word in words:
    #     if word not in sameWord:
    #         sameWord[word] = 1
    #     else:
    #         sameWord[word] += 1
            
    # for i in range(len(words)):
    #     # tf-idf value for query
    #     query.append(math.log(1+((uniqueWords[words[i]])/len(words)), 2)*searchdata.get_idf(words[i]))

    #   # for word in words:
    # #     if word not in sameWord:
    # #         sameWord[word] = 1
            
    # # tf = len(sameWord)/len(words)

    # print("QUERY")
    # print(query)
    # print()
    # print("DOC VECTOR")
    # print(docVector)

    # store words in a list
    words = phrase.split(" ")

    total = len(words)

    print("words before: ")
    print(words)

    sameWord = {}

    for word in words:
        if word not in sameWord:
            sameWord[word] = 1
        else:
            sameWord[word] += 1

    words = []

    for word in sameWord:
        words.append(word)

    print("words after: ")
    print(words)

    # print(sameWord)
    # print("length: " + str(len(sameWord)))

    # contains tf-idf values for all documents 
    docVector = []

    # idf print
    for word in words:
        print(word + ": " + str(searchdata.get_idf(word)))

    # for all documents
    for i in range(len(reverseDict)):
        # temporary storage of tfidf values of a document
        row = []
        # for words in phrase
        for j in words:
            # print(reverseDict[str(i+1)])
            # print("j: " + j)
            # store the tfidf of the word 
            # print("tf-idf: " + str(searchdata.get_tf_idf(reverseDict[str(i+1)], j)))
            row.append(searchdata.get_tf_idf(reverseDict[str(i+1)], j))
        # add row 
        docVector.append(row)

    # list that stores tf-idf value of words inputted
    query = []

    for i in range(len(words)):
        # tf-idf value for query
        print(words[i])
        # print("idf query: " + str(searchdata.get_idf(words[i])))
        tf = sameWord[words[i]]/total
        # print("tf: " + str(tf))
        # print("log: " + str(math.log(1+tf, 2)))
        # print("all:" + str(math.log(1+tf, 2)searchdata.get_idf(words[i])))
        query.append(math.log(1+tf, 2)*searchdata.get_idf(words[i]))

    for line in docVector:
        print(line)
    print()
    print(query)

    # COSINE SIMILARITY CODE
    topSimilarity = []
    cosMap = {}

    # calculating left denominator
    leftDenom = 0
    for j in range(len(query)):
        leftDenom += query[j] * query[j]
    leftDenom = math.sqrt(leftDenom)



    cosSimilarity = []
    for i in range(len(docVector)):
        
        #caculating numerator
        numerator = 0

        for j in range(len(query)):
            numerator += query[j] * docVector[i][j]
        
        #calculating right denominator
        rightDenom = 0
        for j in range(len(query)):
            rightDenom += docVector[i][j]*docVector[i][j]
        rightDenom = math.sqrt(rightDenom)

        denominator = rightDenom * leftDenom

        if(numerator == 0 or denominator == 0):
                similarity = 0
        else:
            similarity = numerator/denominator

            if(boost):
                pageRank = searchdata.get_page_rank(reverseDict[str(i+1)])
                similarity *= pageRank
        
        cosSimilarity.append(similarity)

        if(similarity not in cosMap):
            cosMap[similarity] = []
            cosMap[similarity].append(i + 1)    
        else:
            cosMap[similarity].append(i+1)


    cosSimilarity.sort(reverse=True)

    # print("THIS IS THE MAP")
    # print(cosMap)
    # print()

    #contains dictionary {url, title, score}
    searchResult = []
    sentResults = []

    for i in range(len(cosSimilarity)):

        print(cosMap[cosSimilarity[i]])
        print()
    
        for j in cosMap[cosSimilarity[i]]:
            print("THIS IS SEARCH RESULTS: ")
            print(sentResults)
            if(j not in sentResults):
                print("THIS IS J: " + str(j))        
                url = reverseDict[str(j)]
                title = dict[url].split("_")[1]
                print("TITLE: " + title)
                score = cosSimilarity[i]
                sentResults.append(j)
                break

        searchResult.append({"url": url, "title": title, "score": score})

    print()
    # print(searchResult)

    return searchResult

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
    
# crawler.crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")

# search("kiwi banana peach", False)