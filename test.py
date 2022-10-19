import os

def createFolderFiles(currentFile):

    filePath = os.path.join('crawl', currentFile)

    # create a directory for the url
    # check if the folder with the same name exists
    if os.path.exists(filePath):
        print("currentFile exists in crawl")
    else:
        # if there isn't, make a new folder with a name same as the url
        os.makedirs(filePath)

    # create files within the created folder
    if os.path.isdir(filePath):
        # create two files: words for storing words and url for storing urls
        wordPath = os.path.join(filePath, "words")
        urlPath = os.path.join(filePath, "urls")

        # create an empty word file
        if not os.path.exists(wordPath):
            open(wordPath, "w").close()

        # create an empty url file
        if not os.path.exists(urlPath):
            open(urlPath, "w").close()
        
    return wordPath, urlPath


list = ["I", "love", "V", "he", "is", "my", "husband"]

for index in list:
    word, url = createFolderFiles(index)
    print(word + "\n " + url)