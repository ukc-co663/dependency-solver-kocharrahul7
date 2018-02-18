import json




repository = json.load(open('repository.json'))
initial = json.load(open('initial.json'))
constraints = json.load(open('constraints.json'))

# for key in repository:
# 	print (key)
# print (repository)
# print (initial)
# print (constraints)

mustaddlist = []
toaddlist = []
versionlist = []
typelist = []
conflicts = []

def rec(addlist):
	print(addlist)
	nmlist = []
	verlist = []
	templist = []
	for key in addlist:
		if ">=" in key:
			names, versions = key.split(">=")
		elif "=" in key:
			names, versions = key.split("=")
		nmlist.append(names)

	for key in repository:
		for nmestr in nmlist:
			if key['name']==nmestr:
				templist.append(key)
	for k in templist:
		# print(k)
		if "depends" in k:
			if k["depends"] == []:
				mustaddlist.append(k["name"])



for key in constraints:
	newstr = key[1:]
	mustaddlist.append(newstr)
	print (newstr)
	# toaddlist.append(newstr)
	for key in repository:
		if(key['name']==newstr):
			print (key)
			# print("here")
			if 'depends' in key:
				# print ("dependant")
				for dependancy in key["depends"]:
					print (dependancy)
					if(len(dependancy)==1):
						# print ("must add")	
						mustaddlist.append(dependancy[0])
					else:
						for d in dependancy:
							for k in repository:
								if ">=" in d :
									name, version = d.split(">=")
								elif "=" in d :
									name, version = d.split("=")
								n = 0
								if name == k["name"]:
									# print ("d "+d)
									toaddlist.append(d)
rec(toaddlist)



for name in mustaddlist:
	print ("mustaddlist"+name)


# for name in toaddlist:
# 	print ("toaddlist"+name)


