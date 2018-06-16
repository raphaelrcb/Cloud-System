import socket
import threading
import thread
import sys
import authenticate

def thread_iniciated(connect, client):
    connect.send('OK')
    print 'Concetado por', client

    user,password,login = authenticate.server_login(connect,client)
    #print user, password, login
    if login == 0:
        failed = 'log in not succesfull, please try again'
        #print failed
        connect.send(failed)
        quit()
    # if login == 1:
    #     print 'log in succesfull'
    while True:
        msg = connect.recv(1024)
        if not msg: break
        print client, msg

    connect.close()
    print 'saiu do loop'
    return 'Close'

HOST = ''              # Endereco IP do Servidor
PORT = 5001            # Porta que o Servidor esta
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)

print 'Waiting Connection...'
server_socket.bind(orig)
server_socket.listen(1)

while True:
    connect, client = server_socket.accept()
    try:
        msg = thread.start_new_thread( thread_iniciated,(connect, client))
    except:
        print 'could not create thread'

print 'Finalizando conexao do cliente', cliente
