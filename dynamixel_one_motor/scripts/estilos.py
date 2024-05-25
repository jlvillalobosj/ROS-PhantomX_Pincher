import tkinter as tk
    
# Crear el botón con el estilo personalizado
def creacion_boton(contenedor, texto, color, comando, posx, posy):
    boton = tk.Button(contenedor,text = texto, bg=color, command = comando )
    boton.place(relx=posx, rely=posy, anchor="center")
    return boton



# Crear una barra deslizante
def barra_deslizante(contenedor,id,valor_inicial,valor_final,intervalos,funcion_movimiento_motor,posx , posy):
    tk.Label(contenedor, text=f"Servo: {id}").place (relx=posx, rely=0.05, anchor="n")

    barra = tk.Scale(contenedor, from_=valor_inicial, to=valor_final, orient=tk.VERTICAL, showvalue=0,tickinterval=intervalos, command=funcion_movimiento_motor, length=200, resolution=1)
    barra.place(relx=posx, rely=posy, anchor="n")
    return barra

# Etiqueta para mostrar el valor actual de la barra deslizante
#label_valor = tk.Label(ventana, text="Valor: 0")
#label_valor.pack(pady=10)