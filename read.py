import argparse
import json
import sys



def dependencies(initial,item,repository):
	retlist = []
	templist = []
	# print("asdf")
	# print(item)
	if len(item["depends"]) != 0:
		for temp in (item["depends"]):
			if temp not in initial:
				# print(temp)
				temp = redoList(temp,repository)
				if len(temp) == 1:
					retlist.extend(temp)
				elif len(temp)>1:
					templist.append(temp)
	# print(retlist)

	for items in templist:
		retlist.append(items[0])

	return retlist



def control(initial,inputlst,repository):
	for inp in inputlst:
		if inp not in initial:
			dependencys = []
			if "depends" in inp:
				dependencys = dependencies(initial,inp,repository) #like next configs
				# print(dependencys)
				if len(dependencys)>0:
					temp = control(inputlst,dependencys,repository)
					inputlst = temp + inputlst
	# print(inputlst)
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

	print(finallist)


	
if __name__ == "__main__":
	main()
