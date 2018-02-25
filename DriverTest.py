from os import environ
import os
from subprocess import PIPE, run, Popen, DEVNULL

def green(text):
	return "\033[1;32m{}\033[0;0m".format(text)

def red(text):
	return "\033[1;31m{}\033[0;0m".format(text)

def blue(text):
	return "\033[1;34m{}\033[0;0m".format(text)


def runNegTestCase(argList, isStdin):
	state = "right"
	subPro = None
	if isStdin == False:
		subPro = run(argList, stdin = DEVNULL, stdout = PIPE, stderr = PIPE)
	else:
		subPro = run(["echo", "\"PROGRAM a; END b.\"", "|"]+argList, stdin = PIPE, stdout = PIPE, stderr = PIPE)

	# print(subPro.stdout.decode())
	# print(subPro.stderr.decode())	
	if subPro.stdout.decode() == "" and subPro.stderr.decode() != "":
		print("# NEGATIVE TEST: "+str(argList)+" ...... "+green("Succeed"))
	else:
		print("# NEGATIVE TEST: "+str(argList)+" ...... "+red("Failed"))
	print()

def runPosTestCase(argList, isStdin):
	state = "right"
	subPro = None
	if isStdin == False:
		subPro = run(argList, stdin = DEVNULL, stdout = PIPE, stderr = PIPE)
	else:
		subPro = run(["echo", "\"PROGRAM a; END b.\"", "|"]+argList, stdin = PIPE, stdout = PIPE, stderr = PIPE)

	if subPro.stdout.decode() != "" and subPro.stderr.decode() == "":
		print("# POSITIVE TEST: "+str(argList)+" ...... "+green("Succeed"))
	else:
		print("# POSITIVE TEST: "+str(argList)+" ...... "+red("Failed"))
	print()

if __name__ == "__main__":
	root = os.path.dirname(os.path.abspath("Runner.py"))
	testCaseFolder = root+"/testCaseFolder"
	runNegTestCase(["./sc",  "test.sim"], False)
	runNegTestCase(["./sc"], False)
	runNegTestCase(["./sc", "-e"], False)
	runNegTestCase(["./sc", "-e", "-a", "-a"], False)

	runPosTestCase(["./sc", "-s", "test.sim"], False)
	runPosTestCase(["./sc", "-s"], True)
	runPosTestCase(["./sc", "-c", "test.sim"], False)
	runPosTestCase(["./sc", "-c"], True)
	runPosTestCase(["./sc", "-c", "-g", "test.sim"], False)
	runPosTestCase(["./sc", "-c", "-g"], True)