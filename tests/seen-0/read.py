import json

repository = json.load(open('repository.json'))
initial = json.load(open('initial.json'))
constraints = json.load(open('constraints.json'))

# print (repository)
# print (initial)
# print (constraints)
newlist = []

for key in constraints:
	newstr = key[1:]
	if(">=" in newstr):
		print (newstr.find(">="))
		print ("greaterThanEquals")
	elif("<=" in newstr):
		print (newstr.find("<="))
		print ("lessThanEquals")
	elif(">" in newstr):
		print (newstr.find(">"))
		print ("greaterThan")
	elif("<" in newstr):
		print (newstr.find("<"))
		print ("lessThan")
	elif("=" in newstr):
		print (newstr.find("="))
		print ("Equals")
	else:
		print (newstr.find("="))
		print ("none")

	newlist.append(newstr)

for item in newlist:
	print(item)
