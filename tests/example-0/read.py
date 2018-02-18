import json

repository = json.load(open('repository.json'))
initial = json.load(open('initial.json'))
constraints = json.load(open('constraints.json'))

print (repository[0])
# print (initial)
# print (constraints)


def rec (data,namelist,versionlist,conflicts):
	nl = []
	vl = []
	tl = []
	for y in range(len(data)):
		print(data[y])
		if data[y]["name"] in namelist:
			print ("found it")
			if 'depends' in data[y]:
				dependencies = []
				for x in data[y]["depends"]:
					dependencies.append(x)
				for dependence in dependencies:
					print (dependence)

					for d in dependence:
						if(d not in initial):
							# print (" not in initial")

							tl.append(d)
							if '>=' in d: 
								nl,vl = split(nl,vl,d,">=")
								print (nl[0])
								print (vl[0])
								print (tl[0])
							elif '=' in d:
								nl,vl = split(nl,vl,d,"=")
								print (nl[0])
								print (vl[0])
								print (tl[0])

							else:
								vl.append('')
								nl.append(d)
								print (nl[0])
								print (vl[0])
								print (tl[0])
			else:
				print ("+" + data[y]["name"])
				namelist.remove(data[y]["name"] )
	namelist.extend(nl)
	versionlist.extend(vl)

	rec(data,namelist,versionlist,conflicts)




def split (namelist,versionlist,newstr,constr):
		names, versions = newstr.split(constr)
		namelist.append(names)
		versionlist.append(versions)
		return namelist,versionlist




namelist = []
versionlist = []
typelist = []
conflicts = []

for key in constraints:
	newstr = key[1:]
	# print (newstr)
	location = newstr.find("=")
	namelist.append(newstr)
	versionlist.append('')
	typelist.append('')
	rec(repository,namelist,versionlist, conflicts) #total repository, list of names to be added, and versions of that.

