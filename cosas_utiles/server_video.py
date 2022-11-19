'''
#link con informacion
# http://pymotw.com/2/socket/tcp.html
# https://steelkiwi.com/blog/working-tcp-sockets/


import socket

#CREAMOS TCP SOCKET
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address=('localhost', 50500)
print('starting up on {} port {}'.format(*server_address)) 
sock.bind()    
#bind()->to associate the socket with the server address.

# In this case, the address is localhost, referring to the current server, and the port number is 50500

sock.listen(1)  


list_of_clients=[]
#listen()-> puts the socket into server mode
conn, addr = sock.accept()
#accept()-> waits for an incoming connection
#   returns an open connection between the server and client, along with the address of the client
while 1:
    data = conn.recv(1024)
    # recv()-> Data is read from the connection 
    if not data:
        break
    data=data.decode()
    data+=" its me"
    data=bytes(data,'utf-8')
    conn.sendall(data)
    # sendall() -> Data is  transmitted from the connection
conn.close()
# close() -> When communication with a client is finished, the connection needs to be cleaned up
# 
# '''



import socket
import select
import sys
from _thread import *

#SETEO DEL SOCKET
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR , 1)

#Asignacion IP del Server
IP_addres=str(socket.gethostbyname(socket.gethostname()))

#Puerto de conexion
Port=int(5566)

#Hace binds d a la IP y el puerto , el cliente debe conectarse al mismo IP y puerto
server.bind((IP_addres,Port))

#Escucha hasta 10 conexiones (limite de usuarios)
server.listen(10)

list_of_clients=[]

def clientthread(conn ,addr):

    conn.send("Connexion establecida con server".encode("utf8"))

    while True:
        try:
            message=conn.recv(2048)
            if message:
                '''imporime mensaje de la ip mas el mensaje de la persona que escribe en terminal'''
                print("<"+addr[0]+">"+message)

                #Llamada a bradcast para la fucnion enviar mensaje
        
                broadcast(message,conn)
            else:
                '''el mensaje puede estar vacio si se pierde cenexion o se desconectan del servidor'''
                remove(conn)
        except:
            continue
    
#Usando esta funcion transmitimos el mensaje a todos los clientes
def broadcast(message,connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
                #si la conexion se pierde  se remuee el cliente
                remove(clients)


#elimina el objeto de la lista de clientes
def remove (connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
    
while True:


    conn,addr=server.accept()
    list_of_clients.append(conn)

    print(addr[0]+" connected")
    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()









    





