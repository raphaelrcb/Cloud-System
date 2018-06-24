import socket
import sys
import protocol

def Connected(client_socket, command):
    user, password, login = protocol.client_login(sys.argv, client_socket)
    print 'Seja bem vindo ', user, "!\n Execute o comando 'help' para mais opcoes:"
    path = client_socket.recv(1024)
    while command[0] <> '\x18':
        # server_msg = client_socket.recv(1024)
        # print server_msg
        command = raw_input("What do you wish to do?:~/" + path + " >")
        command = command.split()
        #command = raw_input()
        #command = command.split()

        if command[0] == 'help':
            protocol.help()

        elif command[0] == 'checkdir':
            protocol.cl_checkdir(client_socket, path, command)

        elif command[0] == 'cd' and len(command) > 1:
            if command[1] == '..' and path == 'home_' + user:
                print 'cant do thath'
            path = protocol.cl_cd(client_socket, command, path)

        elif command[0] == 'mv' and len(command) == 3:
            protocol.cl_mv(client_socket, command)

        elif command[0] == 'rm' and len(command) > 1:
            protocol.cl_rm(client_socket,command)

        elif command[0] == 'makedir' and len(command) > 1:
            protocol.cl_makedir(client_socket, command)

        elif command[0] == 'download' and len(command) > 1:
            protocol.cl_download(client_socket, command)

        elif command[0] == 'upload' and len(command) > 1:
            protocol.cl_upload(client_socket, command)

        else:
            print "command does not exists"
    return

check_ip = sys.argv[1].split('.')
if len(check_ip) != 4:
    print "Ip not reconigzed"
    quit()
HOST = sys.argv[1]     # Endereco IP do Servidor
del sys.argv[1]
PORT = 5001            # Porta que o Servidor esta
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest = (HOST, PORT)

client_socket.connect(dest)
hand_shake = client_socket.recv(1024)
msg = 'Hello Server'
if hand_shake == 'OK':
    print 'Connection Stablished'
    Connected(client_socket, msg)
else:
    print 'No connection'

print 'Client closed connection'
client_socket.close()
