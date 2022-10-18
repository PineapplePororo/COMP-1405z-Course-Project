import myqueue
import webdev

def crawl(seed):

    #resets all existing data 
    #performs webcrawl starting at the seed url; parses all pages that cna be reached through linsnks form the see URL
    # gneeratis all data required for other parts of the project and saves that data to files. 

    urlQueue = []

    currURL = ""
    nextURL = myqueue.dequeue(seed)

    while(len(myqueue.isempty(urlQueue)) == False):
        
        currURL = nextURL      

        #adding the text to a words array by splitting the url read by each empty space/newline
        page = webdev.read_url(currURL.split())

        #now we have to go throught the page contents 
        #separate them based on tags (p tag or a tag to get text or links respectively)
        #get the words and put them in a array or file or smthn
        #get the links and enqueue them

        nextURL = myqueue.dequeue(urlQueue)


    return "amongus hehe"


print(webdev.read_url("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))


