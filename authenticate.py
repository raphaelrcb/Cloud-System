import sys

def server_login(connect, client): #The credentials are made when the program starts and are passed as arguments when executing the program (python program.py username password).
#In case the user does not pass any credentials, the program understands a new user is being created
#In case the user pass only his or hers username, the program understands it and asks for the respective password


    users_file = open("users.txt", "a+") #Opens file with username and password of the users (no criptography) if file doesnt exists, create one
    users = users_file.readlines() #Read all the lines of the file, the file is organized by   ##########################################
    username = None                # Setting null values for username and password             #Username1
    password = None                # In case they are nor found in the file                    #password1
    authorization = 0              # Set authorization as 0 in case the user and               #Username2
                                   # the password does not match in the file                   #password2
    for i in range(0, len(users)): #                                                           #...
        users[i] = users[i].strip() #fix the strings

    first_msg = connect.recv(1024)
    if first_msg == 'New User': #None credentials passed, create new username and passwords
        connect.send( 'New User, please create your username and your password\nChoose an username: ')
        username = connect.recv(1024)
        connect.send( 'Now choose a password: ')
        password = connect.recv(1024)

        authorization = 1 #Authorize but then check if the username already exists, if it does, it does not authorize.
        for i in range(0, len(users)):
            if username == users[i]:
                print 'User already exists'
                authorization = 0
                return (username, password, authorization)
        users_file.write(username)
        users_file.write('\n')
        users_file.write(password)
        users_file.write('\n')
        connect.send('succesfull')

    if first_msg == 'Search': #None credentials passed, create new username and passwords
        connect.send('tell me the user')
        username = connect.recv(1024)

        for i in range(0, len(users)): #check if the username is valid (if exists in the database)
            if username == users[i]:
                connect.send ("FOUND\nUser please type in your password: \n")
                password = connect.recv(1024)
                if password == users[i+1]:
                    authorization = 1
                    print 'Log in succesfull'
                    connect.send('succesfull')
                break
        if authorization == 0:
            connect.send("Username not found")

    if first_msg == 'Confirm':
        connect.send('tell me the user and password')
        username = connect.recv(1024)
        password = connect.recv(1024)

        for i in range(0, len(users)):
            if username == users[i]:
                if password == users[i+1]:
                    authorization = 1
                    connect.send('succesfull')
                break
        if authorization == 0:
            connect.send("Login failed")
    # if authorization == 1:
    #     print "Hello User", username, "ypur password is ", password, "\n"
    # if authorization == 0:
    #     print "Log in not authorized, please try again\n"

    users_file.close
    return (username, password, authorization)
#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)
import sys

def client_login(argv, client_socket):

    username = None                # Setting null values for username and password             #Username1
    password = None                # In case they are nor found in the file                    #password1
                                   # the password does not match in the file                   #password2
    if len(argv) < 2: #None credentials passed, create new username and passwords
        client_socket.send('New User')
        server_msg = client_socket.recv(1024)
        print server_msg
        username = raw_input()
        client_socket.send(username)
        server_msg = client_socket.recv(1024)
        print server_msg
        password = raw_input()
        client_socket.send(password)
        if client_socket.recv(1024) == 'log in not succesfull, please try again':
            print 'Usename already exists, pease choose a different one'
            quit()


    if len(argv) == 2: #the user passed the username but not the password
        client_socket.send('Search')
        if client_socket.recv(1024) == 'tell me the user':
            client_socket.send(argv[1])
            username = argv[1]
        server_msg = client_socket.recv(1024)
        print server_msg
        if server_msg == "Username not found": quit()
        password = raw_input()
        client_socket.send(password)
        if client_socket.recv(1024) == 'Username not found':
            print 'Password incorrect'
            quit()

    if len(argv) > 2:
        client_socket.send('Confirm')
        if client_socket.recv(1024) == 'tell me the user and password':
            client_socket.send(argv[1])
            username = argv[1]
            password = argv[2]
            client_socket.send(argv[2])
        if client_socket.recv(1024) == 'Login failed':
            print 'Username or password incorrect'
            quit()

    return username, password, 1
