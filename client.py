import socket
import sys
import authenticate
import client_commands

def Connected(client_socket, command):
    user, password, login = authenticate.client_login(sys.argv, client_socket)
    print 'Seja bem vindo ', user, "!\n Execute o comando 'help' para mais opcoes:"
    while command[0] <> '\x18':
        # server_msg = client_socket.recv(1024)
        # print server_msg
        command = raw_input()
        command = command.split()

        if command[0] == 'help':
            client_commands.help()

        elif command[0] == 'checkdir':
            client_commands.checkdir()

        elif command[0] == 'cd' and len(command) > 1:
            client_commands.cd(command[1])

        elif command[0] == 'mv' and len(command) > 2:
            client_commands.mv(command[1], command[2])

        elif command[0] == 'rm' and len(command) > 1:
            client_commands.rm(command[1])

        elif command[0] == 'makedir' and len(command) > 1:
            client_commands.makedir(command[1])

        elif command[0] == 'upload' and len(command) > 1:
            client_commands.upload(command[1])

        elif command[0] == 'download' and len(command) > 1:
            client_commands.download(command[1])
        else:
            print "command does not exists"

        client_socket.send (command[0])
    return


HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
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
