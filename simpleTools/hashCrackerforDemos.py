#Daniel Santiago
#Simple program that crack hashes using both brute-force methods or dictionary attacks

import md5
import sys
# characters = range(48,57) + range(65,90)+range(97,122)
characters = range(97,122)
def checkPassword(password) :

	m= md5.new(password)
	# print "hash is: " + m.hexdigest()
	if (m.hexdigest()== secHash) :
		print "\nmatch found: [" + password +"]"
		sys.exit()

def recurse(width, position, baseString, disp):
	for char in characters:

		if (position < width -1 ) :
			recurse(width, position+1, str(baseString) + "%c" % char , disp)

		if (disp):
			sys.stdout.write("\rTarget secHash [" + secHash + "] string: " + baseString + "%c" %char )
			sys.stdout.flush()
		checkPassword(baseString + "%c" %char )

def brute_force(disp) :
	maxChars = 32
	for baseWidth in range(1,maxChars+1) :
		if disp:
			print "checking passwords with " + str(baseWidth) + " letters"
		recurse(baseWidth, 0, "", disp)

def dictionary():
	for line in File.readlines() :
		word = (line)
		# print "trying: " + word
		sys.stdout.write("trying: " + word)
		sys.stdout.flush()

		checkPassword(line.strip("\n"))


secHash = raw_input("Input MD5 secHash: ")
options = input("choose method: 1=brute, 0=dict \n")
disp = bool(input("Display output ? (0=no, 1=yes) \n"))

if (options == 1 ) :
	brute_force(disp)

else :
	if (options == 0 ) :
		File = open("ES.dic" )
		dictionary()
	else :
		print "wrong"
