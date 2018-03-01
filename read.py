import argparse
import json
import sys

def dependencies(initial,item,repository):
	retlist = []
	templist = []
	conflicts = []
					
	if len(item["depends"]) != 0:
		for temp in (item["depends"]):
			if temp not in initial:
				temp = redoList(temp,repository)
				if len(temp) == 1:
					if "conflicts" in temp:
						if len(temp["conflicts"])>0:
							conflicts = redoListC(temp["conflicts"],repository)
														
					retlist.extend(conflicts)
					retlist.extend(temp)
				elif len(temp)>1:
					templist.append(temp)
	for conf in conflicts:
		for repo in repository:
			if (repo["name"] == conf["name"] and (conf["versiontype"] =='' or eval(repo["version"]+conf["versiontype"]+conf["version"]))):
				print("asdf")
	emptyList = []



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
			if (repo["name"] == name and (versiontype =='' or eval(repo["version"]+versiontype+version))):
				temp = repo
				temp["operation"] = operation
				retlist.append(temp)
	return retlist 


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
			if (repo["name"] == name and (versiontype =='' or eval(repo["version"]+versiontype+version))):
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
		finallist.append(str(temp));
	# [item.encode('utf-8') for item in finallist]
	
	print(finallist)


	
if __name__ == "__main__":
	main()