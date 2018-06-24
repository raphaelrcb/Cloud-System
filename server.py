import socket
import threading
import thread
import sys
import protocol
import os

def thread_iniciated(connect, client, server_path):
    connect.send('OK')
    print 'Concetado por', client
    user,password,login = protocol.server_login(connect,client, server_path)

    current_path = server_path
    path = ["home_"]


    path[0] = path[0] + user
    client_path = path[0]
    current_path = current_path + '/' + path[0]

    if login == 0:
        failed = 'log in not succesfull, please try again'
        connect.send(failed)
        quit()
    if login == 2:
         protocol.makedir(path[0],server_path)
         os.chdir(current_path)
         #send relative path
    if login == 1:
        if os.path.isdir(current_path):
            os.chdir(current_path)
        else:
            protocol.makedir(path[0], server_path)
            os.chdir(current_path)

    connect.send(client_path)
    while True:

        command = connect.recv(1024)
        print client, command
        if command == 'checkdir':
            protocol.checkdir(connect, current_path)
        if command == 'cd':
            command = connect.recv(1024)
            command = command.split(";")
            current_path, client_path = protocol.cd(current_path, client_path, command, path)
            connect.send(client_path)
        if command == 'makedir':
            command = connect.recv(1024)
            protocol.makedir(command, current_path)
        if command == 'rm':
            file = connect.recv(1024)
            protocol.rm(file, current_path)
        if command == 'mv':
            command = connect.recv(1024)
            command = command.split(";")

            protocol.mv(command[0], command[1], current_path, server_path)

        if command == 'download':
            protocol.download(connect)

        if command == 'upload':
            protocol.upload(connect, current_path)


        if not command: break

    connect.close()
    return 'Close'

HOST = ''              # Endereco IP do Servidor
PORT = 5001            # Porta que o Servidor esta
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
server_path = os.getcwd()


print 'Waiting Connection...'
server_socket.bind(orig)
server_socket.listen(1)

while True:
    connect, client = server_socket.accept()
    try:
        msg = thread.start_new_thread( thread_iniciated,(connect, client, server_path))
    except:
        print 'could not create thread'

print 'Finalizando conexao do cliente', cliente
