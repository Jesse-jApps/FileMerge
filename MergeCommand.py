#!/usr/bin/env python

import os, sys, getopt, shutil
import ntpath

from GitWrapper import GitWrapper

# GIT Logic:

# Usage:
# MergeCommand -o <originalfile> -n <newfile> -p <projdir>
# Outcome: The newfile will be properly updated and can then overwrite the original file

# For this to work, original and new need to be at some point identical
# Thus this command should be run on complete new data creation


class MergeCommand(object):
	"""docstring for MergeCommand"""
	def __init__(self):
		super(MergeCommand, self).__init__()

	def runCommand(self, original, new, project):

		# Create merging folder structure if doesn't exist yet
		# It lives inside the project dir
		basePath = os.path.join(project, '.mergingstruct/')
		newVersion = os.path.join(basePath, 'new/')
		originalVersion = os.path.join(basePath, 'original/')
		repo = os.path.join(basePath, 'repo.git/')
		
		gitOriginalFile = os.path.join(originalVersion, ntpath.basename(original))
		gitNewFile = os.path.join(newVersion, ntpath.basename(new))


		gitManager = GitWrapper(repo)

		# Copy original
		if not os.path.isdir(originalVersion):
			os.makedirs(originalVersion)
			gitManager.initDir(originalVersion)
		shutil.copy(original, originalVersion)

		# Copy also origin first to new
		if not os.path.isdir(newVersion):
			os.makedirs(newVersion)
			gitManager.initDir(newVersion)
		shutil.copy(new, newVersion)




		# Add new to repo
		print "Push new"
		gitManager.pushFile(gitNewFile)

		# Commit original file
		print "Commit original"
		gitManager.commitFile(gitOriginalFile)

		# Pull original for newVersion her might come a merging conflict
		print "Pull in original"
		gitManager.mergeTheirs(originalVersion)

		# Push merged Version
		print "push original"
		gitManager.pushFile(gitOriginalFile)

		gitManager.pull(newVersion)






		# Copy Merged version to very originals
		shutil.copy(gitNewFile, original)
		shutil.copy(gitNewFile, new)



def main():

	original = ""
	new = ""
	project = ""

	help = 'MergeCommand.py -o <originalfile> -n <newfile> -p <projdir>'

	try:
		opts, args = getopt.getopt(sys.argv[1:],"ho:n:p:",["ofile=","nfile=", "pdir="])
	except getopt.GetoptError:
		print help
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print help
			sys.exit(0)
		elif opt in ("-o", "--ofile"):
			original = arg
		elif opt in ("-n", "--nfile"):
			new = arg
		elif opt in ("-p", "--pdir"):
			project = arg

	MergeCommand.runCommand(original, new, project)

	sys.exit(0)




if __name__ == "__main__":
	main()
