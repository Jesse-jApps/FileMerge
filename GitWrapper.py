import os, sys, commands, subprocess, ntpath

class GitWrapper(object):
	"""docstring for GitWrapper"""
	def __init__(self, repo):
		super(GitWrapper, self).__init__()
		self.repo = repo

		if not os.path.isdir(repo):
			os.makedirs(repo)
			self._runGitCommand(['--bare', 'init'], repo)
		
	
	def initDir(self, dirPath):
		if not os.path.isdir(os.path.join(dirPath, '.git/')):
			self._runGitCommand(['init'], dirPath)
			# Add remote
			self._runGitCommand(['remote', 'add', 'origin', self.repo], dirPath)
			#self.pull(dirPath)
		else:
			print "Is already initialized"


	def commitFile(self, filePath):
		# Add File
		self._runGitCommand(['add', ntpath.basename(filePath)], ntpath.dirname(filePath))
		# Commit File
		self._runGitCommand(['commit', '-m', 'orgVersion'], ntpath.dirname(filePath))

	def pushFile(self, filePath):
		self.commitFile(filePath)
		self.pull(ntpath.dirname(filePath))
		# Push File
		self._runGitCommand(['push', '-u', 'origin', 'master'], ntpath.dirname(filePath))


	def pull(self, dirPath):
		self._runGitCommand(['pull', 'origin', 'master'], dirPath)


	def mergeOurs(self, dirPath):
		self._runGitCommand(['fetch'], dirPath)
		self._runGitCommand(['merge', '--strategy-option', 'ours'], dirPath)

	def mergeTheirs(self, dirPath):
		self._runGitCommand(['fetch'], dirPath)
		self._runGitCommand(['merge', '--strategy-option', 'theirs'], dirPath)

	def _runGitCommand(self, args, dirPath):
		pr = subprocess.Popen(['git'] + args, cwd = dirPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(out, error) = pr.communicate()


		if error:
			print "Error : " + str(error) 
			print "out : " + str(out)
