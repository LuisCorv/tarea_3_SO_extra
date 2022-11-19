
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
import sys
import socket
import json

from tkinter import *
from tkinter import ttk
import tkinter as tk

from PIL import ImageGrab

#################### FUNCIONES DE SOCKET ###########

def recieve():
    while True:
        print("ALGO HA SIDO RECIVIDO")
        try:
            mensaje=client_socket.recv(2048)
            mensaje.decode()
            mensaje=json.loads(mensaje)
            print(mensaje)
            if mensaje[0]=="linea":#tipo,curr_x,curr_y,x,y,texto(opcional)
                addLine(mensaje)
            if mensaje[0]=="texto":
                textoCaja(mensaje)
            if mensaje[0]=="borrar":
                new_canvas()
            else:
                pass
        except OSError:
            break

def env(data):
    data=json.dumps(data)
    data=data.encode()
    client_socket.send(data)


#################### FUNCIONES DE PIZARRA ###########
def locate_xy(work):
    global current_x ,current_y
    current_x=work.x
    current_y=work.y

def show_color(new_color):
    global color
    color=new_color

##ESCRITURA
tempt_linex=0
tempt_liney=0
def addLine(info):
    canvas.create_line((float(info[1]),float(info[2]),float(info[3]),float(info[4])),width=float(info[5]),fill=color,capstyle=ROUND,smooth=TRUE)

def new_canvas():
    canvas.delete('all')
    display_pallete()

def textoCaja(info):
    data=info[5]
    canvas.create_text(info[1],info[2],text=data, fill="black", font=('Helvetica 20'))
    cajaTexto.delete(0,len(data))

##ENVIO

def env_addLine(work):
    global current_x,current_y,color
    data=["linea",current_x,current_y,work.x,work.y,get_current_value(),color]
    current_x,current_y=work.x, work.y
    env(data)

def env_new_canvas():
    data=["borrar"]
    env(data)

def env_textoCaja(work):
    texto=cajaTexto.get()
    cajaTexto.delete(0,len(texto))
    current_x=work.x
    current_y=work.y
    data=["texto",current_x,current_y,work.x,work.y,texto]
    print("ENVIADO")
    env(data)


###### PIZARRA#####

root=Tk() #ventana

#icon
root.title("White duck Board")

root.geometry("1050x570+150+50")
root.configure(bg="#f2f3f5")
root.resizable(False,False)

imagen_icon=PhotoImage(file="logo.png")
root.iconphoto(False,imagen_icon)

current_x= 0
current_y= 0
color='black'

#colocar boton para borrar toda la pizarra
eraser=PhotoImage(file="goma_borrar.png")
Button(root,image=eraser,bg="#f2f3f5",command=env_new_canvas).place(x=30,y=400)

#Definir lugar para los colores al lado
colors=Canvas(root,bg="#ffffff",width=37,height=300,bd=0)
colors.place(x=30,y=60)
def display_pallete():   
    id= colors.create_rectangle((10,10,30,30),fill='black')
    colors.tag_bind(id,'<Button-1>',lambda x: show_color('black'))

    id= colors.create_rectangle((10,40,30,60),fill='gray')
    colors.tag_bind(id,'<Button-1>',lambda x: show_color('gray'))

    id= colors.create_rectangle((10,70,30,90),fill='brown4')
    colors.tag_bind(id,'<Button-1>',lambda x: show_color('brown4'))

    id= colors.create_rectangle((10,100,30,120),fill='red')
    colors.tag_bind(id,'<Button-1>',lambda x: show_color('red'))

    id= colors.create_rectangle((10,130,30,150),fill='orange')
    colors.tag_bind(id,'<Button-1>',lambda x: show_color('orange'))

    id= colors.create_rectangle((10,160,30,180),fill='yellow')
    colors.tag_bind(id,'<Button-1>',lambda x: show_color('yellow'))
    
    id= colors.create_rectangle((10,190,30,210),fill='green')
    colors.tag_bind(id,'<Button-1>',lambda x: show_color('green'))

    id= colors.create_rectangle((10,220,30,240),fill='blue')
    colors.tag_bind(id,'<Button-1>',lambda x: show_color('blue'))

    id= colors.create_rectangle((10,250,30,270),fill='purple')
    colors.tag_bind(id,'<Button-1>',lambda x: show_color('purple'))

display_pallete()

#Colocar pizzarra
canvas=Canvas(root,width=930,height=500,background="white",cursor="hand2")
canvas.place(x=100,y=10)


canvas.bind('<Button-1>',locate_xy)
canvas.bind('<B1-Motion>',env_addLine)

#Slider(GROSOR TRAZO)
current_value= tk.DoubleVar()

def get_current_value():
    return '{: .2f}'.format(current_value.get())

def slider_changed(event):
    value_label.configure(text=get_current_value())

slider=ttk.Scale(root,from_=0,to=100,orient='horizontal',command=slider_changed, variable=current_value)
slider.place(x=30,y=530)

#value label
value_label= ttk.Label(root,text=get_current_value())
value_label.place(x=27,y=550)

#texto
cajaTexto = tk.Entry(root,font="Helvetica 15")
cajaTexto.place(x=400,y=530)

canvas.bind('<Control-Button-1>',env_textoCaja)

#save
def save_board():
    global canvas
    x=root.winfo_rootx()+canvas.winfo_x()+50
    y=root.winfo_rooty()+canvas.winfo_y()+10
    x1=x+canvas.winfo_width()+270
    y1=y+canvas.winfo_height()+150
    ImageGrab.grab().crop((x,y,x1,y1)).save("algo.png")

guardado=PhotoImage(file="Save-icon.png")
Button(root,image=guardado,bg="#f2f3f5",command=save_board).place(x=30,y=450)



#############SOCKET#######################
#Creacion de socket
IP_server=socket.gethostbyname(socket.gethostname())
Puerto=int(5566)
ADDR=((IP_server, Puerto))
client_socket=socket.socket(AF_INET,SOCK_STREAM)
client_socket.connect(ADDR)



#Hilo con el server

recieve_thread=Thread(target=recieve)
recieve_thread.start()


root.mainloop()


