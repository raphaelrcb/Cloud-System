import socket
HOST = ''              # Endereco IP do Servidor
PORT = 5001            # Porta que o Servidor esta

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
server_socket.bind(orig)
server_socket.listen(1)
print 'Waiting Connection...'
while True:
    connect, cliente = server_socket.accept()
    connect.send('OK')

    print 'Concetado por', cliente
    while True:
        msg = connect.recv(1024)
        if not msg: break
        print cliente, msg
    connect.close()
    break

print 'Finalizando conexao do cliente', cliente
