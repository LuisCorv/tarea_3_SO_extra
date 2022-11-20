#link con informacion
# http://pymotw.com/2/socket/tcp.html
# https://steelkiwi.com/blog/working-tcp-sockets/
import time

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

#Escucha  (limite de usuarios)
server.listen()

num_conect=0
action_reg=[]
list_of_clients=[]

##########FUNCIONES#######
def clientthread(conn):
    global num_conect
    if num_conect>1:
        sync_pizarra(conn)
    
    data=str("Sync")
    conn.send(data.encode("utf8"))

    while True:
        try:
            mensaje=conn.recv(2048)
            action_reg.append(mensaje)
            broadcast(mensaje)
        except:
            list_of_clients.remove(conn)
            conn.close()
            print("Se ha ido un cliente")
            num_conect=num_conect-1
            print(f"El numero de conexiones actual es:{num_conect}")
            break

def broadcast(mensaje):
    for clients in list_of_clients:
            clients.send(mensaje)
            
def sync_pizarra(conn):
    for message in action_reg:
        time.sleep(0.00000001)
        conn.send(message)


#######CODIGO 
print("Servidor activado , iniciando operaciones")
while 1:
    print(f"El numero de conexiones actual es:{num_conect}")
    if num_conect>=5:
        conn,addr=server.accept()
        data=str("Denied")
        conn.send(data.encode("utf8"))
        conn.close()
    else:
        num_conect+=1
        conn,addr=server.accept()
        list_of_clients.append(conn)
        print(addr[0]+" connected")
        thread=threading.Thread(target=clientthread,args=(conn,))
        thread.start()
    
conn.close()
# close() -> When communication with a client is finished, the connection needs to be cleaned up


