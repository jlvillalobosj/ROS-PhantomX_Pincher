import tkinter as tk
import estilos
import rospy
import interface
from tkinter import messagebox
from PIL import ImageTk, Image
__author__ = "Julin L. Villalobos J - Jhonnathan A. Gómez V."
__credits__ = []
__email__ = "jlvillalobosj@unal.edu.co - jagomezv@unal.edu.co"
__status__ = "Test"

class InterfacePresentation:


    def __init__(self):
        self.screen = tk.Tk()
        self.screen.title("Phantom X  Pincher - UN")
        self.screen.geometry("700x500")


        # Cargar la imagen
        imagen = Image.open("/home/julianv/catkin_ws/src/dynamixel_one_motor/scripts/Images/homeImage.jpg")
        resized_image = imagen.resize((700, 500), Image.BILINEAR)  # Ajustar al tamaño de la ventana
        self.photo = ImageTk.PhotoImage(resized_image)

        # Crear una etiqueta (Label) y establecer la imagen como fondo
        background_label = tk.Label(self.screen, image=self.photo, compound=tk.CENTER, width=500, height=500)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label_titulo = tk.Label(self.screen, text="Manipulador robot Phantom X - Pincher", font=("Yu Mincho Demibold", 18, "bold"),bg = "blue", fg="white")

        self.label_titulo.place(relx=0.5, rely=0.1, anchor="center")

        # Cuadro de información
        self.label_info = tk.Label(self.screen, text=__author__ , bg="blue",fg="white")
        self.label_info.place(relx=0.5, rely=0.9, anchor="center")

        self.label_info = tk.Label(self.screen, text=__email__ , bg="blue",fg="white")
        self.label_info.place(relx=0.5, rely=0.96, anchor="center")

        # Cuadro de introduccion
        texto = '''La presente aplicación tiene por objetivo realizar el control de movimiento de un brazo robótico Phantom X - Pincher, 
        esta cuenta con 5 posicones específicas y control de movimiento en cada articulación'''

        self.label_parrafo = tk.Label(self.screen, text=texto, wraplength=250, bg="blue", fg="white", font=("Arial", 12, "bold"))
        self.label_parrafo.place(relx=0.7, rely=0.5, anchor="center")

        boton_start = estilos.creacion_boton(self.screen,"Inicio", '#00FF00', self.boton_push_start, 0.9, 0.9)
        self.screen.mainloop()

    def boton_push_start(self):
        self.screen.destroy()
        interface.main()

    def boton_push_start(self):
        # Intenta inicializar rospy y muestra un mensaje indicando el estado de la conexión
        try:
            rospy.init_node('PhantomX_Movement')
            self.screen.destroy()
            interface.main()
        except Exception:
            messagebox.showerror("Error de conexión", "No se pudo establecer la conexión con el Phantom X")
            pass


        