import sys
import os
import shutil


def server_login(connect, client, server_path): #The credentials are made when the program starts and are passed as arguments when executing the program (python program.py username password).
    #In case the user does not pass any credentials, the program understands a new user is being created
    #In case the user pass only his or hers username, the program understands it and asks for the respective password
    users_file = open(server_path + "/users.txt", "a+") #Opens file with username and password of the users (no criptography) if file doesnt exists, create one
    users_file.seek(0)

    users = users_file.readlines() #Read all the lines of the file, the file is organized by   ##########################################
    # print users
    username = None                # Setting null values for username and password             #Username1
    password = None                # In case they are nor found in the file                    #password1
    authorization = 0              # Set authorization as 0 in case the user and               #Username2
    i = 0                               # the password does not match in the file                   #password2

    for i in range(0, len(users)): #                                                           #...
        users[i] = users[i].strip() #fix the strings

    first_msg = connect.recv(1024)
    if first_msg == 'New User': #None credentials passed, create new username and passwords
        connect.send( 'New User, please create your username and your password\nChoose an username: ')
        username = connect.recv(1024)
        connect.send( 'Now choose a password: ')
        password = connect.recv(1024)

        authorization = 2 #Authorize but then check if the username already exists, if it does, it does not authorize.
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
        print username, password

        #print 'oi'
        #print users
        for i in range(0, len(users)):
        #    print 'oi2'
        #    print users[i]
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
    users_file.seek(0)
    users_file.close()
    return (username, password, authorization)
    #print "Number of arguments: ", len(sys.argv)
    #print "The arguments are: " , str(sys.argv

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

def upload(connect, current_path):
    #print "download ", command[1]
    connect.send('sync')
    file_name = connect.recv(1024)
    file_name = file_name.split('/')
    file_name = current_path + '/' + file_name[-1 ]
    # print('receiving data...')
    with open(file_name, 'wb') as f:
        while True:
            data = connect.recv(1024)
            # print data, '----'
            if (not data) or (data == 'eof'):
                break
            f.write(data)
            connect.send('sync')
        #print 'saiu do while '
        f.close()
        # print 'transfer completer\n'
        #    connect.send('transfer complete')
    # if connect.recv(1024) == 'sync':
    #     print 'deu certp'
    return

def download(connect):
    connect.send('sync')
    file_name = connect.recv(1024)
    #print file_name

    transfer = open(file_name,'rb')
    l = transfer.read(1024)
    while (l):
       connect.send(l)
       l = transfer.read(1024)
       if connect.recv(1024) != 'sync':
           print 'something went wrong'
           break
       #print('Sent ',repr(l))
    transfer.close()
    connect.send('eof')

    return

def checkdir(connect, path):
    files =  os.listdir(path)
    if not  files:
        connect.send('[]')
    if files:
        files = "/".join(files)
        connect.send(files)
    return

def cd(current_path,  client_path, command, path):

    temp = command[1].split('/')

    for x in range(0, len(temp)):
        if not os.path.isdir(temp[x]):
            return current_path, client_path

    if temp[0] == '..' and client_path != path[0]:
        current_path = current_path.split('/')
        client_path = client_path.split('/')
        for i in range(0,len(temp)):
            current_path.pop()
            client_path.pop()
            path.pop()
        current_path = "/".join(current_path)
        client_path = "/".join(client_path)
    if temp[0] != "..":
            for i in range(0, len(temp)):
                path.append(temp[i])
                current_path = current_path + '/' + temp[i]
                client_path = client_path + '/' + temp[i]

    os.chdir(current_path)
    return current_path, client_path

def mv(org_file, dest_dir, current_path, server_path):
    if (os.path.isdir(org_file) or os.path.isfile(org_file)) and (os.path.isdir(server_path + "/" + dest_dir) or os.path.isfile( server_path + "/" + dest_dir)):
        shutil.move(current_path + "/" + org_file, server_path + "/" + dest_dir)
    return

def rm(file, current_path):
    if os.path.isdir(file):
        if os.listdir(current_path + '/' + file) == []:
            os.rmdir(file)
        elif os.listdir(current_path + '/' + file) != []:
            shutil.rmtree(file)
    if os.path.isfile(file):
        os.remove(file)

    return

def makedir(dirname, path):
    os.chdir(path)
    os.mkdir(dirname)
    return

def help():
    print "-----Lista de Comandos----"
    print "- checkdir -> apresenta as pastas e arquivos presentes no diretorio corrente."
    print "- cd path_to_dir -> permite acesso ao diretorio 'path_to_dir.'"
    print "- mv org_file dest_dir -> move 'org_file' para o diretorio 'path_to_dir'."
    print "- rm file -> remove o arquivo ou diretorrio de nome 'file'."
    print "- makedir dirname -> cria um nove diretorio de nome 'dirname'."
    print "- upload path_to_file -> faz o upload de um arquivo em 'path_to_file' para o servidor."
    print "- download file -> faz o download do arquivo 'file' para a sua maquina"
    print "- CTRL+X -> Sai do programa e fecha a conexao"
    return

def cl_checkdir(client_socket, path, command):
    client_socket.send(command[0])
    files = client_socket.recv(1024)
    if files != '[]':
        files = files.split('/')
    print '\n', files, '\n'
    # client_socket.send(path)
    return

def cl_cd(client_socket, command, path):
    client_socket.send(command[0])
    command = ";".join(command)
    client_socket.send(command)
    path = client_socket.recv(1024)

    return path

def cl_mv(client_socket, command):#command[1] = org_file
    client_socket.send(command[0])
    client_socket.send(command[1] + ';' + command[2])
    return

def cl_rm(client_socket, command):
    client_socket.send(command[0])
    client_socket.send(command[1])
    return

def cl_makedir(client_socket,command):
    client_socket.send(command[0])
    client_socket.send(command[1])
    return

def cl_upload(client_socket, command):
    # print "upload file from ", command[1]
    client_socket.send(command[0])

    if client_socket.recv(1024) == 'sync':
        client_socket.send(command[1])
        transfer = open(command[1],'rb')

        l = transfer.read(1024)
        while (l):
            client_socket.send(l)
            l = transfer.read(1024)
            if client_socket.recv(1024) != 'sync':
                print 'something went wrong'
                break
    transfer.close()
    client_socket.send('eof')
    return

def cl_download(client_socket, command):

    client_socket.send(command[0])
    if client_socket.recv(1024) == 'sync':
        client_socket.send(command[1])
        print('receiving data...')
        with open(command[1], 'wb') as f:
            while True:
                data = client_socket.recv(1024)
                #print data, '----'
                if (not data) or (data == 'eof'):
                    break
                f.write(data)
                client_socket.send('sync')
        f.close()
    print 'transfer completer\n'
    return
