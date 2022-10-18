# Alvina Han (Kayeon) 
# 10/14/22
# Tutorial 5 Problem 1: Improving Runtime Complexity

import random
import time

# add an element to the end
def addend(list, dict, value):

	# add value to end of list
	list.append(value)

	# check if value is in dict
	if value in dict:
		# if yes, increment frequency by 1 
		dict[value] += 1
	else:
		# else, make a new key and have frequency = 1
		dict[value] = 1


# remove element from the start
def removestart(list, dict):

	# if empty list(dict), nothing to remove
	if len(list) == 0:
		return None

	# remove element from start of the list
	value = list.pop(0)
		
	# if the frequency of the value is bigger than one
	if dict[value] > 1:
		# decrement
		dict[value] -= 1
	else:
		# remove the existing key
		del dict[value]

	# return the value removed
	return value
	

# determine if an item exists in the list
def containslinear(list, value):

	# loop for every index
	for index in list:
		# check if they equal
		if value == index:
			return True

	return False
	

# determine if an item exists in the dict
def containshash(dict, value):
	
	# loop for every key
	for key in dict:
		# check if they equal
		if key == value:
			return True
	
	return False


# test 1
'''
list = []
hash = {}
for i in range(25):
	if random.randint(0,100) < 75:
		num = random.randint(0,10)
		print("Adding", num)
		addend(list,hash,num)
	else:
		num = removestart(list,hash)
		print("Removed", num)
	print(list)
	print(hash)
'''

# test 2
'''
list = []
hash = {}
addprob = 100
removeprob = 90
repeat = 50000
maxval = 500
searchlist = []
#randomly build the data by probabilistically adding/removing items to the list
#also generate a list of items to search for later
#also make sure that the dictionary search is returning the same result as the list search
for i in range(repeat):
	if random.randint(0,100) < addprob:
		addend(list, hash, random.randint(0,maxval))
	if random.randint(0,100) < removeprob:
		removestart(list, hash)
		
	searchlist.append(random.randint(0,maxval))
	
	searchnum = random.randint(0,maxval)
	
	if containslinear(list, searchnum) != containshash(hash, searchnum):
		print("Error: dictionary and list search returned different results")
		exit()

start = time.time()
for i in searchlist:
	containslinear(list, i)
end = time.time()
print("Linear time: ", (end-start))

start = time.time()
for i in searchlist:
	containshash(hash, i)
end = time.time()
print("Hash time: ", (end-start))
'''