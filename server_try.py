import socket
import thread

#HOST = ''              # Endereco IP do Servidor
port = 5000            # Porta que o Servidor esta
i=0
server_socket = socket.socket()     # Create socket
server_host = socket.gethostname()  # Get local machine name

server_socket.bind((server_host,port)) # Bind socket to port
server_socket.listen(1)              # Start listening for Connection

print 'Waiting for Connection...'

while True:
    conn, client = server_socket.accept() # Establish connection with client
    print 'connection established with ', client
    msg = 'a'
    conn.send(msg)
    print 'message to client sent '

#    conn.close()
