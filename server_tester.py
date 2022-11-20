#link con informacion
# http://pymotw.com/2/socket/tcp.html
# https://steelkiwi.com/blog/working-tcp-sockets/

import socket
#import select
#import sys
from _thread import *
import json
import threading

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
server.listen()

list_of_clients=[]

##########FUNCIONES#######
def clientthread(conn):
    while True:
        try:
            mensaje=conn.recv(2048)
            broadcast(mensaje)
        except:
            remove(conn)
            #conn.close()
            break

def broadcast(mensaje):
    for clients in list_of_clients:
            clients.send(mensaje)
            

def remove (connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
#######CODIGO 
print("Servidor activado , iniciando operaciones")
while 1:
    conn,addr=server.accept()
    list_of_clients.append(conn)

    print(addr[0]+" connected")


    thread=threading.Thread(target=clientthread,args=(conn,))
    thread.start()
    #start_new_thread(target=clientthread,args=(conn,))
    
conn.close()
# close() -> When communication with a client is finished, the connection needs to be cleaned up


