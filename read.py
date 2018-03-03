import argparse
import json
import sys
from pkg_resources import parse_version

def dependencies(initial,item,repository):
	retlist = []
	templist = []
	if len(item["depends"]) != 0:
		for temp in (item["depends"]):
			if temp not in initial:
				temp = redoList(temp,repository)
				if len(temp) == 1:
					if "conflicts" in temp:
						if len(temp["conflicts"])>0:
							redoListC(temp["conflicts"])
					retlist.extend(temp)
				elif len(temp)>1:
					templist.append(temp)
	emptyList = []
	for item in retlist:
		emptyList = redoList(item["conflicts"],repository)

	for ds in templist:
		z=0
		for c,d in enumerate(ds,0):
			for item in emptyList:
				if d != item: 
					# print (c,d)
					z=c
		retlist.append(ds[z])

	return retlist






def control(initial,inputlst,repository):
	for inp in inputlst:
		if inp not in initial:
			dependencys = []
			if "depends" in inp:
				dependencys = dependencies(initial,inp,repository)#like next configs
				# print(dependencys)
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
				retlist.append(temp)
	return retlist 

def solve(ver1,vert,ver2,):
	s1="\""+str(ver1)+"\""
	s2="\""+str(ver2)+"\""
	if(vert=="<"):
		return parse_version(s1) < parse_version(s2)
	elif(vert==">"):
		return parse_version(s1) > parse_version(s2)
	elif(vert=="<="):
		return parse_version(s1) <= parse_version(s2)
	elif(vert==">="):
		return parse_version(s1) >= parse_version(s2)
	elif(vert=="=="):
		return parse_version(s1) == parse_version(s2)



def redoListC(lst):
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
				retlist.append(temp)
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
	for c in constrList:
		temp = c["operation"]+c["name"]+"="+c["version"]
		finallist.append(temp);

	print(json.dumps(finallist))


	
if __name__ == "__main__":
	main()