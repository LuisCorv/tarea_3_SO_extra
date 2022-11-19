
'''import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50500))
# connect()->  to attach the socket directly to the remote address.
mesage='Hello, world'
mesage=bytes(mesage,'utf-8')
s.sendall(mesage)
 # sendall() -> Data is  transmitted from the connection
data = s.recv(1024)
# recv()-> Data is read from the connection 
s.close()
# close() -> When communication with a client is finished, the connection needs to be cleaned up
print ('Received', repr(data))'''


from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread
import tkinter
import sys
import socket
top=tkinter.Tk()
top.title("ALGOOOO")

def recieve():
    while True:
        try:
            mensaje=client_socket.recv(BUFSIZ).decode("utf8")
            mensaje_list.insert(tkinter.END,mensaje)
        except OSError:
            break

def send(event=None):
    mensaje=mi_ms.get()
    mi_ms.set("")
    client_socket.send(bytes(mensaje))
    mensaje_list.insert(tkinter.END,mensaje)

messages_frame=tkinter.Frame(top)
mi_ms=tkinter.StringVar()
mi_ms.set("")
scrollbar=tkinter.Scrollbar(messages_frame)

#Contenido Area mensaje

mensaje_list=tkinter.Listbox(messages_frame,height=25,width=50,yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
mensaje_list.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
mensaje_list.pack()
messages_frame.pack()

#Area o campo para escribir y  boton enviar 

entryfield=tkinter.Entry(top,textvariable=mi_ms)
entryfield.bind("<Return>",send)
entryfield.pack()
send_button=tkinter.Button(top,text="ENVIAR",command=send)
send_button.pack()


#Creacion de socket
IP_server=socket.gethostbyname(socket.gethostname())
Puerto=int(5566)
BUFSIZ=1024
ADDR=((IP_server, Puerto))
client_socket=socket.socket(AF_INET,SOCK_STREAM)
client_socket.connect(ADDR)



#Hilo con el server

recieve_thread=Thread(target=recieve)
recieve_thread.start()
tkinter.mainloop()