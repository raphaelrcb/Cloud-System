import socket
HOST = ''              # Endereco IP do Servidor
PORT = 5001            # Porta que o Servidor esta

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
server_socket.bind(orig)
server_socket.listen(1)
while True:
    con, cliente = server_socket.accept()
    con.send('OK')

    print 'Concetado por', cliente
    while True:
        msg = con.recv(1024)
        if not msg: break
        print cliente, msg
    con.close()
    break

print 'Finalizando conexao do cliente', cliente
