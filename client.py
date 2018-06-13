import socket

def Connected(client_socket, msg):
    while msg <> '\x18':
        
        client_socket.send (msg)
        msg = raw_input()

    return


HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5001            # Porta que o Servidor esta
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest = (HOST, PORT)

client_socket.connect(dest)
print 'Para sair use CTRL+X\n'

hand_shake = client_socket.recv(1024)

msg = 'Hello Server'
if hand_shake == 'OK':
    print 'Connection Stablished'
    Connected(client_socket, msg)

client_socket.close()
