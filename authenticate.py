import sys

print "This is the name of the script: ", sys.argv[0]

if len(sys.argv) < 2:
    print "New User"
if len(sys.argv) == 2:
    print "User ", sys.argv[1], "please type in your password: \n"

if len(sys.argv) > 2 and len(sys.argv) < 4:
    print "Hello User", sys.argv[1], "ypur password is ", sys.argv[2], "\n"
else:
    print "Number of arguments invalid"

#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)
