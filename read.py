import argparse
import json
import sys
from distutils.version import LooseVersion

globalConflict = []
globalDepends = []


def dependencies(initial,item,repository):
	retlist = []
	templist = []
	conflist = []
	if len(item["depends"]) != 0:
		for temp in (item["depends"]):
			if temp not in globalDepends:
				temp = redoList(temp,repository)
				if len(temp) == 1:
					if temp[0] not in globalDepends:
						retlist.extend(temp)
						globalDepends.extend(temp)
				elif len(temp)>1:
					if temp not in templist:
						templist.append(temp)
	for t in templist:
		for s in t:
			if s in globalDepends:
				break
			elif s in globalConflict:
				t.remove(s)
		for ds in t:
			deplist = []
			conlist = []
			bothlist = []
			if "conflicts" not in ds and "depends" not in ds:
				retlist.extend(temp)
				globalDepends.extend(temp)
				break
			elif "conflicts" not in ds:
				deplist.append(ds)
			elif "depends" not in ds:
				conlist.append(ds)
			else:
				bothlist
			if len(deplist)==1:
				retlist.extend(deplist)
				break
			elif len(conlist)==1:
				retlist.extend(conlist)
			elif len(bothlist)==1:
				retlist.extend(bothlist)
	return retlist




def conf(initial,item,repository):
	retlist = []
	templist = []
	conflist = []
	if len(item["conflicts"]) != 0:
		temp = (item["conflicts"])
		tmp = redoListC(temp,repository)
		for z in tmp:
			x = z
			x["operation"] = '+'
			if x in globalDepends or x in initial:
				x["operation"] = '-'
				retlist.append(z)
				globalConflict.append(z)
	return retlist




def dealWithDepends(lst,repository,initial):
	templist = []
	finallist = []
	for item in lst:
		interemList = []
		for i in item["depends"]:
			interemList.append(redoList(i,repository))
		finallist.append(interemList)

	for f in finallist:
		if f in initial:
			finallist.remove(f)


	min = 99999
	z = 0;
	for c,thing in enumerate(finallist,0):
		if(len(thing)<min):
			min = len(thing)
			z = c

	retlist = []
	retlist.extend(finallist[z][0])
	retlist.append(lst[z])
	return(retlist)

def dealWithConflicts(lst,repository,initial):
	templist = []
	finallist = []
	for item in lst:
		if item not in initial:
			finallist.append(redoListC(item["conflicts"],repository))
	min = 99999
	z = 0;

	for c,thing in enumerate(finallist,0):
		if(len(thing)<min):
			min = len(thing)
			z = c
	retlist = []
	retlist.append(finallist[z][0])
	retlist.append(lst[z])
	return(retlist)


def control(previous,inputlst,repository):
	for inp in inputlst:
		dependencys = []
		conflicts = []
		if "depends" in inp:
			dependencys = dependencies(previous,inp,repository)
			if len(dependencys)>0:
				temp = control(inputlst,dependencys,repository)
				inputlst = temp + inputlst
		if "conflicts" in inp:
			conflicts = conf(previous,inp,repository)
			if len(conflicts)>0:
				temp = control(inputlst,conflicts,repository)
				inputlst = temp + inputlst
	return inputlst





def redoList(lst,repository):
	retlist = []
	for item in lst:
		if "operation" not in item:
			if(item[0] == '+' or item[0] == '-'):
				operation = item[0]
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
		templist = []
		for repo in repository:
			if (repo["name"] == name and (versiontype =='' or solve(str(repo["version"]), versiontype, str(version)))):
				temp = repo
				temp["operation"] = operation
				templist.append(temp)
		item = templist[0]
		if(len(templist)>1):
			for t in templist:
				if t["size"]<item["size"]:
					item = t
		retlist.append(item)
	return retlist 

# def removeMulIns():

def solve(ver1,vert,ver2,):
	s1="\""+str(ver1)+"\""
	s2="\""+str(ver2)+"\""
	if(vert=="<"):
		return LooseVersion(ver1) < LooseVersion(ver2)
	elif(vert==">"):
		return LooseVersion(ver1) > LooseVersion(ver2)
	elif(vert=="<="):
		return LooseVersion(ver1) <= LooseVersion(ver2)
	elif(vert==">="):
		return LooseVersion(ver1) >= LooseVersion(ver2)
	elif(vert=="=="):
		return LooseVersion(ver1) == LooseVersion(ver2)



def redoListC(lst,repository):
	retlist = []
	for item in lst:
		operation = "-"
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
		templist = []
		for repo in repository:
			if (repo["name"] == name and (versiontype =='' or solve(str(repo["version"]), versiontype, str(version)))):
				temp = repo
				temp["operation"] = operation
				retlist.append(temp)
	return retlist 

def removeDupes(lst):
	retlist = []
	for l in lst:
		if l not in retlist:
			retlist.append(l)
	return retlist


def main():
	def json_from_file(file_path):
		with open(file_path) as f:
			return json.load(f)

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("repository_arg", type=json_from_file)
	parser.add_argument("initial_arg", type=json_from_file)
	parser.add_argument("constraints_arg", type=json_from_file)
	args = parser.parse_args()

	repository = (args.repository_arg)
	initial = (args.initial_arg)
	constraints = (args.constraints_arg)

	initial = redoList(initial,repository)
	init = initial 

	constraints = redoList(constraints,repository)
	constrList = control(initial,constraints,repository)

	constrList = removeDupes(constrList)

	finallist = []
	for c in constrList:
		temp = c["operation"]+c["name"]+"="+c["version"]
		finallist.append(temp);

	print(json.dumps(finallist))



	
if __name__ == "__main__":
	main()