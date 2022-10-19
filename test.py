import os

def manageFolder():
    # create a folder that will contain all the folders from the crawl
    if os.path.exists("crawl"):
        # if it's created already, check if there are files in the folder

        # create a list of folders/files in the crawl folder
        dirs = os.listdir("crawl")

        # loop for all the subfolders in the crawl folder
        for dir in dirs:
            # store the path of the subfolder
            subfolderPath = os.path.join("crawl", dir)

            # make a list of all files in the subfolder
            files = os.listdir(subfolderPath)

            # loop for all the files in subfolder
            for file in files:
                # remove every file
                os.remove(os.path.join(subfolderPath, file))
            # remove the subfolder
            os.rmdir(subfolderPath)
    else:
        # if there isn't, make a new folder 
        os.makedirs("crawl")

manageFolder()