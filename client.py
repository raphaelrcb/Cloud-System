import socket
import sys
import authenticate
import client_commands

def Connected(client_socket, msg):
    user, password, login = authenticate.client_login(sys.argv, client_socket)
    print 'Seja bem vindo ', user, "!\n Execute o comando 'help' para mais opcoes:"
    while msg <> '\x18':
        # server_msg = client_socket.recv(1024)
        # print server_msg
        client_socket.send (msg)
        msg = raw_input()
        if msg == 'help':
            client_commands.help()

    return


HOST = '127.0.0.1'     # Endereco IP do Servidor
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
