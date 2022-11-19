import tkinter


#crea la ventana
ventana= tkinter.Tk()

#Dimensiona la ventana
ventana.geometry("600x600")  #ancho , alto


#etiqueta=tkinter.Label(ventana,text="Hola mundo",bg="grey")
#etiqueta.pack(fill=tkinter.X) #posiciona los objetos sin especificar donde van/sire para colocar objetos en puntos especificos (investigar)


cajaTexto = tkinter.Entry(ventana,font="Helvetica 15")
cajaTexto.pack()


def textoCaja():
    result=cajaTexto.get()
    print(result)

boton1 = tkinter.Button(ventana,text="click",command=textoCaja)
boton1.pack()

#loop principal del programa
ventana.mainloop()