import searchdata
import json
import os
import crawler
import math

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
    

# crawler.crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")

# search("kiwi banana peach", False)