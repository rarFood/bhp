import md5
import sys
characters = range(97,122)
def checkPassword(password) :

	m= md5.new(password)
	if (m.hexdigest()== hash) :
		print "match [" + password +"]"
		sys.exit()

def recurse(width, position, baseString):
	for char in characters:
		if (position < width -1 ) :
			recurse(width, position+1, str(baseString) + "%c" % char )

		checkPassword(baseString + "%c" %char )
		#print "Target Hash [" + hash + "string: " + baseString

def brute_force() :
	maxChars = 32
	for baseWidth in range(1,maxChars+1) :
		#print "checking passwords width [" + str(baseWidth) + "]"
		recurse(baseWidth, 0, "")

def dictionary():
	for line in File.readlines() :
		# print("checking: "+ line)
		checkPassword(line.strip('\n'))


hash = raw_input("Input MD5 hash: ")
options = input("choose method: 1=brute, 0=dict")

if (options == 1 ) :
	brute_force()

else :
	if (options == 0 ) :
		File = open("dict.txt" )
		dictionary()
	else :
		print "wrong"
