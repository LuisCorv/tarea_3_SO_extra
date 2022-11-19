#link con informacion
# http://pymotw.com/2/socket/tcp.html
# https://steelkiwi.com/blog/working-tcp-sockets/

import socket
import select
import sys
from _thread import *
import json

##########SETEO DE SOCKET#####

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
server.listen(2)
list_of_clients=[]

##########FUNCIONES#######
def clientthread(conn ,addr):
    while True:
        try:
            mensaje=conn.recv(2048)
            mensaje.decode()
            mensaje=json.loads(mensaje) #recibo lista con datos (idea=> [accion realizada, dato1,dato2,dato n])
            if mensaje[0]=="linea":
                broadcast(mensaje,conn)
            if mensaje[0]=="texto":
                print("RECIBIDO")
                broadcast(mensaje,conn)
            if mensaje[0]=="borrar":
                broadcast(mensaje,conn)

        except:
            continue

def broadcast(mensaje,connection):
    for clients in list_of_clients:
            try:
                print("AQUI")
                mensaje=json.dumps(mensaje)
                mensaje=mensaje.encode()
                clients.send(mensaje)
            except:
                clients.close()
                #si la conexion se pierde  se remuee el cliente
                remove(clients)

def remove (connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
#######CODIGO 
while 1:
    conn,addr=server.accept()
    list_of_clients.append(conn)
    print(addr[0]+" connected")
    start_new_thread(clientthread,(conn,addr))
    
conn.close()
# close() -> When communication with a client is finished, the connection needs to be cleaned up


