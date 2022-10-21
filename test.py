import os

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


def createFiles(currentFile):

    manageFolder()

    # store path for the subfolder of the current file
    filePath = os.path.join('crawl', currentFile)

    # create an empty word file
    if not os.path.exists(filePath):
        open(filePath, "w").close()

    return filePath

createFiles("1_N-4")