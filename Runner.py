from os import environ
import os
from subprocess import PIPE, run, Popen, DEVNULL

def green(text):
	return "\033[1;32m{}\033[0;0m".format(text)

def red(text):
	return "\033[1;31m{}\033[0;0m".format(text)

def blue(text):
	return "\033[1;34m{}\033[0;0m".format(text)

def runTestCase(sim_file, ans_file):
	state = "right"
	# sim_file = "test.sim"
	print("\n--------------- %s -----------------"%sim_file)
	# ans_file = "test.scanner"
	subPro = run(["./sc", "-s", sim_file], stdin = DEVNULL, stdout = PIPE, stderr = PIPE)
	
	resList = subPro.stdout.decode().split('\n')
	# print(resList)
	err_in_res = ""
	err_in_ans = ""

	with open(ans_file,'r') as f:
		ans_str = f.read()
	ansList= ans_str.split('\n')
	# print(ansList)

	for res_i in resList:
		if res_i.startswith("error: "):
			err_in_res = res_i
			resList.remove(res_i)
		if res_i == "":
			resList.remove(res_i)

	for ans_i in ansList:
		if ans_i.startswith("error: "):
			err_in_ans = ans_i
			ansList.remove(ans_i)
		if ans_i == "":
			ansList.remove(ans_i)


	for res_i in resList:
		if res_i not in ansList:
			print(red("- "+res_i))
			state = "wrong"

	for ans_i in ansList:
		if ans_i not in resList:
			print(green("+ "+ans_i))
			state = "wrong"

	print(blue("@resErr: "+err_in_res))
	print(blue("@ansErr: "+err_in_ans))
	if err_in_ans == "" and err_in_res != "":
		state = "wrong"
	if err_in_ans != "" and err_in_res == "":
		state = "wrong"

	print("^^^^^^^^^^^^^^^^^^^ %s ^^^^^^^^^^^^^^^^^^^^^\n"%state)
	return state

if __name__ == "__main__":
	root = os.path.dirname(os.path.abspath("Runner.py"))
	testCaseFolder = root+"/testCaseFolder"
	caseList = os.listdir(testCaseFolder)
	simList = []
	for curFileName in caseList:
		if ".sim" in curFileName:
			cleanName = curFileName[0:len(curFileName)-4]
			if cleanName not in simList:
				simList.append(cleanName)
	print(simList)
	assert len(simList)*2 == len(caseList)

	ansList = []

	for tmpName in simList:
		ansList.append(runTestCase("testCaseFolder/"+tmpName+".sim", "testCaseFolder/"+tmpName+".scanner"))

	wrongCnt = 0
	for ans in ansList:
		if ans == "wrong":
			wrongCnt+=1
	print("========================================")
	print(red(str(wrongCnt))+"/"+green(str(len(ansList)))+" is wrong!")
	print("========================================")
