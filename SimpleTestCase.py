import os, sys, getopt

from MergeCommand import MergeCommand


# Simple TestCase with XML files
# 
# Goal of this test is to apply changes in generated.xml to original.xml
# Both files start as same files
# During the test original.xml will change frequently while generated.xml sometimes
def main():

	basePath = os.path.dirname(os.path.realpath(__file__))
	testfolder = os.path.join(basePath, 'testresources/')

	original = os.path.join(testfolder, 'original/data.xml')
	generated = os.path.join(testfolder, 'new/data.xml')

	projectPath = os.path.join(testfolder, 'project/')

	merger = MergeCommand()
	print testfolder
	merger.runCommand(original, generated, projectPath)

	sys.exit(0)




if __name__ == "__main__":
	main()
