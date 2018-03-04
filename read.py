import argparse
import json
import sys
from distutils.version import LooseVersion



def dependencies(initial,item,repository):
	retlist = []
	templist = []
	conflist = []

	if len(item["depends"]) != 0:
		for temp in (item["depends"]):
			if temp not in initial:
				temp = redoList(temp,repository)
				if len(temp) == 1:
					if "conflicts" in temp:
						if len(temp["conflicts"])>0:
							conflist.extend(redoListC(temp["conflicts"]))
					retlist.extend(temp)
				elif len(temp)>1:
					templist.append(temp)
	emptyList = []
	for item in retlist:
		if "conflicts" in item:
			if len(item["conflicts"])>0:
				emptyList.extend(redoListC(item["conflicts"],repository))
	
	for item in emptyList:
		retlist.append(item)
	

	for ds in templist:
		noConflictList = []
		haveConflictsList = []
		conflictedIndependent=[]
		conflictedDependent=[]
		noConflictedIndependent=[]
		noConflictedDependent=[]
		finalList = []
		for d in ds:
			if("conflicts" not in d):
				noConflictList.append(d)
			else:
				haveConflictsList.append(d)

		if(len(noConflictList)==1):
			retlist.extend(noConflictList)
		elif(len(noConflictList)>1):
			for noConflict in noConflictList:
				if("depends" not in noConflict):
					noConflictedIndependent.append(noConflict)
				else:
					noConflictedDependent.append(noConflict)
		elif(len(haveConflictsList)==1):
			retlist.extend(haveConflictsList[0])
		elif(len(haveConflictsList)>1):
			for haveConflicts in haveConflictsList:
				if("depends" not in haveConflicts):
					conflictedIndependent.append(haveConflicts)
				else:
					conflictedDependent.append(haveConflicts)

		if(len(noConflictedIndependent)>=1):
			if(noConflictedIndependent[0] not in initial):
				retlist.append(noConflictedIndependent[0])
		elif(len(noConflictedDependent)>=1):
			retlist.extend(dealWithDepends(noConflictedDependent,repository,initial))
		elif(len(conflictedIndependent)>=1):
			retlist.extend(dealWithConflicts(conflictedIndependent,repository,initial))
		elif(len(conflictedDependent)>=1):
			retlist.extend(dealWithConflicts(conflictedDependent,repository,initial))


	return retlist


def conf(initial,item,repository):
	retlist = []
	templist = []
	conflist = []

	if len(item["conflicts"]) != 0:
		for temp in (item["conflicts"]):
			if temp not in initial:
				temp = redoListC(temp,repository)
				retlist.extend(temp)


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
		if inp not in previous:
			dependencys = []	
			if "depends" in inp:
				dependencys = dependencies(previous,inp,repository)
				if len(dependencys)>0:
					temp = control(inputlst,dependencys,repository)
					inputlst = temp + inputlst
			elif "conflicts" in inp:
				dependencys = conf(previous,inp,repository)
				if len(dependencys)>0:
					temp = control(inputlst,dependencys,repository)
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

		for repo in repository:
			if (repo["name"] == name and (versiontype =='' or solve(str(repo["version"]), versiontype, str(version)))):
				temp = repo
				temp["operation"] = operation
				if len(retlist)==0:
					retlist.append(temp)
				
				for c,ret in enumerate(retlist,0):
					if  temp["name"]==ret["name"]:
						if temp["size"] < ret["size"]:
							retlist.remove(ret)
							retlist.insert(c,temp)
					else:
						retlist.append(temp)
						# fix remove dupes and then call it here
	return retlist 

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
		for repo in repository:
			if (repo["name"] == name and (versiontype =='' or solve(str(repo["version"]), versiontype, str(version)))):
				temp = repo
				temp["operation"] = operation
				if len(retlist)==0:
					retlist.append(temp)
				for c,ret in enumerate(retlist,0):
					if  temp["name"]==ret["name"]:
						if temp["size"] < ret["size"]:
							retlist.remove(ret)
							retlist.insert(c,temp)
					else:
						retlist.append(temp)
	return retlist 

def removeDupes(lst):
	retlist = []
	for item in lst:
		if item not in retlist:
			retlist.append(item)
	return retlist

def removeUnecessary(lst,initial):#removes all unncessary conflicts
	templst = initial + lst;
	retlist = []
	for c,temp in enumerate(templst,0):
		if temp["operation"] != "-":
			retlist.append(temp)
		else:
			for z in templst[:(c)]:
				if z["name"] == temp["name"] and z["operation"] != temp["operation"]:
					retlist.append(z)
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
	constraints = redoList(constraints,repository)
	constrList = control(initial,constraints,repository)
	finallist = []

	constrList = removeDupes(constrList)
	constrList = removeUnecessary(constrList,initial)

	for c in constrList:
		temp = c["operation"]+c["name"]+"="+c["version"]
		finallist.append(temp);

	print(json.dumps(finallist))


	
if __name__ == "__main__":
	main()