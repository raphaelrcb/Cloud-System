import socket

#HOST = '127.0.0.1'     # Endereco IP do Servidor
#PORT = 5000            # Porta que o Servidor esta

client_socket = socket.socket()
client_host = socket.gethostname()
port = 5000

client_socket.connect((client_host, port))
client_socket.send('Hello')

while True:
    print 'Connected '
    message_received = client_socket.recv(1024)
    if not message_received: break
    print message_received

client_socket.close()
print 'connection closed'
