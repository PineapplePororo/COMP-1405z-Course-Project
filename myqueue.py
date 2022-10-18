# Omar Shah
# September 26/2022
# Tutorial 3: Problem 1 Implementing a Queue

maxLen = 10 # max length of the queue (defaulted to 10)

def isempty(queue):
    
    #queue is empty if length is 0 (nothing in the queue)
    if(len(queue) == 0):
        return True
    else:
        return False

def enqueue(queue, value):
    if(len(queue) == maxLen):
        return False
    else:
        queue.append(value)
        return True

def dequeue(queue):

    if(isempty(queue)):
        return None
    else: 
        return queue.pop(0)


def peek(queue):

    if(isempty(queue)):
        return None
    else:
        return queue[0]

def multienqueue(queue, items):

    counter = 0
    while(len(queue) != maxLen):
        enqueue(queue, items.pop(0))
        counter += 1

    return counter

def multidequeue(queue, number):
    
    dequeueList = []
    
    # if the number trying to be dequed is greater than the amount of items in the queue then setting 
    # number to the length of queue (to dequeue everything)
    if(number > len(queue)):
        number = len(queue)

    for x in range(number):
        dequeueList.append(dequeue(queue))


    return dequeueList
