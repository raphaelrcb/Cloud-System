import socket

def Connected(tcp, msg):
    while msg <> '\x18':

        tcp.send (msg)
        msg = raw_input()
        
    return


HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5001            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dest = (HOST, PORT)

tcp.connect(dest)
print 'Para sair use CTRL+X\n'
msg = raw_input()

ack = tcp.recv(1024)

if ack == 'OK':
    print 'ACK received'
    Connected(tcp, msg)

tcp.close()
