import json

# pass both lists to ensure that you can see everything that is installed(or going to be installed). 
# deapth 1st search instead of my current method.
# 


repository = json.load(open('repository.json'))
initial = json.load(open('initial.json'))
constraints = json.load(open('constraints.json'))

operations = []
names = []
versions = []
versiontypes = []
constraintslist = []
initiallist = []


mustaddlist = []
toaddlist = []





def dependencies(totalList,item):
	# print (item)
	retlist = []
	if len(item["depends"]) != 0:
		for temp in (item["depends"]):
			if temp not in totalList:
				temp = redoList(temp)
				retlist.append(temp)
	deplist = []
	for dependency in retlist:
		# print(len(dependency))
		z = 0
		if len(dependency)>1:
			for i,dep in enumerate(dependency):
				if dep in (totalList):
					z = i
		# print(dependency[z])
		deplist.append(dependency[z])
		# print(type(dependency[z]))
	return deplist



	



def redoList(lst):
	retlist = []
	for item in lst:

		if(item[0] == '+' or item[0] == '-'):
			operation = (item[0])
			tempstr = item[1:]
		else:
			operation = "+"
			tempstr = item
		
		if ">=" in tempstr:
			versiontype = ">="
			name, version = tempstr.split(">=")
		elif "<=" in tempstr:
			versiontype = "<="
			name, version = tempstr.split("<=")
		elif ">" in tempstr:
			versiontype = ">"
			name, version = tempstr.split(">")
		elif "<" in tempstr:
			versiontype = "<"
			name, version = tempstr.split("<")
		elif "=" in tempstr:
			versiontype = "=="
			name, version = tempstr.split("=")
		else:
			name = tempstr;
			version = ''
			versiontype = ''
		for repo in repository:
			if (repo["name"] == name and (versiontype =='' or eval(repo["version"]+versiontype+version))):
				temp = repo
				temp["operation"] = operation
				retlist.append(temp)
	return retlist 


def control(totalList,inputlst):
	for inp in inputlst:
		# print(inp)
		dependencys = []
		if "depends" in inp:
			dependencys = dependencies(totalList,inp)#like next configs
		if len(dependencys)>0:
			temp = control(totalList,dependencys)
			# print(temp)
			inputlst.extend(temp)
	return inputlst


constraints = redoList(constraints)
initial = redoList(initial)
current = []
constrList = control(initial,constraints)
# print(constrList)
finalstr = "["
for c in constrList:
	finalstr+=("\n,"+c["operation"]+c["name"]+"="+c["version"])
finalstr+="]"

print(finalstr)