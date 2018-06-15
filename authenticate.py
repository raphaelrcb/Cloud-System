import sys

def login(): #The credentials are made when the program starts and are passed as arguments when executing the program (python program.py username password).
#In case the user does not pass any credentials, the program understands a new user is being created
#In case the user pass only his or hers username, the program understands it and asks for the respective password


    users_file = open("users.txt", "a+") #Opens file with username and password of the users (no criptography) if file doesnt exists, create one
    users = users_file.readlines() #Read all the lines of the file, the file is organized by   ##########################################
    username = None                # Setting null values for username and password             #Username1
    password = None                # In case they are nor found in the file                    #password1
    authorization = 0              # Set authorization as 0 in case the user and               #Username2
                                   # the password does not match in the file                   #password2
    for i in range(0, len(users)):
        users[i] = users[i].strip() #fix the strings

    if len(sys.argv) < 2: #None credentials passed, create new username and passwords
        print 'New User, please create your username and your password\nChoose an username: '
        username = raw_input()
        print 'Now choose a password: '
        password = raw_input()

        authorization = 1 #Authorize but then check if the username already exists, if it does, it does not authorize.
        for i in range(0, len(users)):
            if username == users[i]:
                print 'User already exists'
                authorization = 0

    if len(sys.argv) == 2: #the user passed the username but not the password
        for i in range(0, len(users)): #check if the username is valid (if exists in the database)
            if sys.argv[1] == users[i]:

                print 'User found' #if the user exists, asks for the password and validate it
                print "User ", sys.argv[1], "please type in your password: \n"
                username = sys.argv[1]
                password = raw_input()
                if password == users[i+1]:
                    authorization = 1
                break

    if len(sys.argv) > 2 and len(sys.argv) < 4:
        username = sys.argv[1]
        password = sys.argv[2]

        for i in range(0, len(users)):
            if username == users[i]:
                print 'User found'
                if password == users[i+1]:
                    authorization = 1
                break

    if authorization == 1:
        print "Hello User", username, "ypur password is ", password, "\n"
    if authorization == 0:
        print "Log in not authorized, please try again\n"

    users_file.close
    return (username, password, authorization)

#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)
