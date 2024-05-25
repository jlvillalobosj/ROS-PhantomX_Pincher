import tkinter as tk
from tkinter import messagebox
import estilos
import math
import jointMovement

class PhantomXPincherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PhantomX - Pincher")
        self.master.geometry("500x500")
        
        # Entrada de texto
        self.entry_text_servo = []
        for i in range(5):
            entry = tk.Entry(self.master, width=4)
            entry.place(relx=((8)*((2*i)+1))/100, rely=0.55, anchor="nw")
            entry.insert(0, str(0))
            entry.bind("<Return>", lambda event, index=i: self.actualizar_valor_desde_entry(index))
            self.entry_text_servo.append(entry)

        # Funcionamiento botones
        self.home_Position = [0,0,0,0,0]
        self.object_Position = [25, 25, 20, -20, 0]
        self.position1 = [-35,35, -30, 30, 0]
        self.position2 = [85, -20, 55, 25, 0]
        self.position3 = [80, -35, 55, -45, 0]
        self.position_servos = [0, 0, 0, 0, 0]

        #Ejecutar en la posición home solo al inicio
        for joint in range(len(self.home_Position)):
            jointMovement.jointMovement(joint+1,self.home_Position[joint])

        # Creacion botones de posiciones específicas
        self.boton_home = estilos.creacion_boton(self.master, "Home", 'green', self.boton_presionado_home, 0.1, 0.7)
        self.boton_object = estilos.creacion_boton(self.master, "Objeto", 'red', self.boton_presionado_object, 0.1, 0.78)
        self.boton_position1 = estilos.creacion_boton(self.master, "Posición 1", 'gray', self.boton_presionado_posicion1, 0.3, 0.66)
        self.boton_position2 = estilos.creacion_boton(self.master, "Posición 2", 'gray', self.boton_presionado_posicion2, 0.3, 0.74)
        self.boton_position3 = estilos.creacion_boton(self.master, "Posición 3", 'gray', self.boton_presionado_posicion3, 0.3, 0.82)

        # Creacion slice de movimientode servomotores
        self.barra_deslizante_servo = []
        self.barra_deslizante_servo += [estilos.barra_deslizante(self.master,1,180,-180,45,self.barra_deslizante_servo1,0.08,0.1)]
        self.barra_deslizante_servo += [estilos.barra_deslizante(self.master,2,60,-60,15,self.barra_deslizante_servo2,0.24,0.1)]
        self.barra_deslizante_servo += [estilos.barra_deslizante(self.master,3,120,-30,30,self.barra_deslizante_servo3,0.4,0.1)]
        self.barra_deslizante_servo += [estilos.barra_deslizante(self.master,4,120,-120,30,self.barra_deslizante_servo4,0.56,0.1)]
        self.barra_deslizante_servo += [estilos.barra_deslizante(self.master,5,40,-70,10,self.barra_deslizante_servo5,0.72,0.1)]

        # Etiquetas posición y rotación del efector final
        self.label_position = []
        self.label_rotation = []

        self.text_label_position = ["X: ", "Y: ", "Z: "]
        self.text_label_rotation = ["Ro: ", "Pi: ", "Ya: "]
        for i in range(3):
            label = tk.Label(self.master, text=self.text_label_position[i] + str(self.posicion_efector_final(self.home_Position)[i]), font=("Helvetica", 14, "bold"))
            label2 = tk.Label(self.master, text=self.text_label_rotation[i]+ str(self.rotacion_efector_final(self.home_Position)[i]), font=("Helvetica", 14, "bold"))

            label.place(relx=0.8, rely=0.66+(i*0.08), anchor="nw")
            label2.place(relx=0.6, rely=0.66+(i*0.08), anchor="nw")

            self.label_position.append(label)
            self.label_rotation.append(label2)

    def actualizar_valor_desde_entry(self, index):
        valor = self.entry_text_servo[index].get()
        try:
            valor = int(valor)
            if valor <= self.barra_deslizante_servo[index].cget('from') and valor >= self.barra_deslizante_servo[index].cget('to'):
                self.barra_deslizante_servo[index].set(valor)  # Actualizar la posición de la barra
            else:
                messagebox.showinfo("","Estas fuera del rango permitido, por favor ingrese otro")

            self.entry_text_servo[index].delete(0, tk.END)  # Eliminar el contenido del Entry
        except ValueError:
            messagebox.showinfo("","Este no es un valor numérico, por favor ingrese otro")
            self.entry_text_servo[index].delete(0, tk.END)  # Eliminar el contenido del Entry

    def matriz_parametros_pincher(self, theta):
        d = [4.5, 0, 0, 0, 11]
        a = [0, 10, 10, 0, 0]
        offset = [0, -90, 0, -90, 0]
        alpha = [-90, 0, 0, -90, 0]
        return jointMovement.mth_tcp(theta, d, a, alpha, offset)

    def posicion_efector_final(self, theta):
        posicion = [fila[3] for fila in self.matriz_parametros_pincher(theta)[:3]]
        for i in range(len(posicion)):
            posicion[i] = round(posicion[i],2)
        return posicion

    def rotacion_efector_final(self, theta):
        rotacion = self.matriz_parametros_pincher(theta)

        yaw = math.atan2(rotacion[2][1], rotacion[2][2])
        yaw = round(math.degrees(yaw),1)

        pitch = math.atan2(rotacion[2][0],math.sqrt((rotacion[2][1])**2 + (rotacion[2][2])**2) )
        pitch = round(math.degrees(pitch),1)

        roll = math.atan2(-rotacion[0][1], rotacion[0][0])
        roll = round(math.degrees(roll),1)

        return [roll, pitch, yaw]

    # Funcionamiento botones
    def boton_presionado_home(self):
        for joint in range(len(self.home_Position)):
            self.entry_text_servo[joint].insert(0, str(self.home_Position[joint]))
            self.barra_deslizante_servos[joint+1](self,self.home_Position[joint]) # Actualiza la barra deslizante con el valor obtenido
            self.barra_deslizante_servo[joint].set(self.home_Position[joint]) # Establece el valor en la barra deslizante
        for i in range(3):
            self.label_position[i].config(text=self.text_label_position[i] + str(self.posicion_efector_final(self.home_Position)[i]))
            self.label_rotation[i].config(text=self.text_label_rotation[i] + str(self.rotacion_efector_final(self.home_Position)[i]))

    def boton_presionado_object(self):
        for joint in range(len(self.object_Position)):
            self.entry_text_servo[joint].insert(0, str(self.object_Position[joint]))
            self.barra_deslizante_servos[joint+1](self, self.object_Position[joint])  # Actualiza la barra deslizante con el valor obtenido
            self.barra_deslizante_servo[joint].set(self.object_Position[joint])  # Establece el valor en la barra deslizante
        for i in range(3):
            self.label_position[i].config(text=self.text_label_position[i] + str(self.posicion_efector_final(self.object_Position)[i]))
            self.label_rotation[i].config(text=self.text_label_rotation[i] + str(self.rotacion_efector_final(self.object_Position)[i]))

    def boton_presionado_posicion1(self):
        for joint in range(len(self.position1)):
            self.entry_text_servo[joint].insert(0, str(self.position1[joint]))
            self.barra_deslizante_servos[joint+1](self, self.position1[joint]) 
            self.barra_deslizante_servo[joint].set(self.position1[joint])
        for i in range(3):
            self.label_position[i].config(text=self.text_label_position[i] + str(self.posicion_efector_final(self.position1)[i]))
            self.label_rotation[i].config(text=self.text_label_rotation[i] + str(self.rotacion_efector_final(self.position1)[i]))

    def boton_presionado_posicion2(self):
        for joint in range(len(self.position2)):
            self.entry_text_servo[joint].insert(0, str(self.position2[joint]))
            self.barra_deslizante_servos[joint+1](self, self.position2[joint])  
            self.barra_deslizante_servo[joint].set(self.position2[joint])
        for i in range(3):
            self.label_position[i].config(text=self.text_label_position[i] + str(self.posicion_efector_final(self.position2)[i]))
            self.label_rotation[i].config(text=self.text_label_rotation[i] + str(self.rotacion_efector_final(self.position2)[i]))

    def boton_presionado_posicion3(self):
        for joint in range(len(self.position3)):
            self.entry_text_servo[joint].insert(0, str(self.position3[joint]))
            self.barra_deslizante_servos[joint+1](self, self.position2[joint]) 
            self.barra_deslizante_servo[joint].set(self.position3[joint])
        for i in range(3):
            self.label_position[i].config(text=self.text_label_position[i] + str(self.posicion_efector_final(self.position3)[i]))
            self.label_rotation[i].config(text=self.text_label_rotation[i] + str(self.rotacion_efector_final(self.position3)[i]))

    # Desplazamiento barras deslizante de los servomotores por funciones
    def barra_deslizante_servo1(self, valor):
        self.entry_text_servo[0].delete(0, tk.END)
        self.entry_text_servo[0].insert(0, str(valor))
        jointMovement.jointMovement(1, int(valor))
        self.position_servos[0] = int(valor)
        for i in range(3):
            self.label_position[i].config(text=self.text_label_position[i] + str(self.posicion_efector_final(self.position_servos)[i]))
            self.label_rotation[i].config(text=self.text_label_rotation[i] + str(self.rotacion_efector_final(self.position_servos)[i]))

    def barra_deslizante_servo2(self, valor):
        self.entry_text_servo[1].delete(0, tk.END)
        self.entry_text_servo[1].insert(0, str(valor))
        jointMovement.jointMovement(2, int(valor))
        self.position_servos[1] = int(valor)
        for i in range(3):
            self.label_position[i].config(text=self.text_label_position[i] + str(self.posicion_efector_final(self.position_servos)[i]))
            self.label_rotation[i].config(text=self.text_label_rotation[i] + str(self.rotacion_efector_final(self.position_servos)[i]))

    def barra_deslizante_servo3(self, valor):
        self.entry_text_servo[2].delete(0, tk.END)
        self.entry_text_servo[2].insert(0, str(valor))
        jointMovement.jointMovement(3, int(valor))
        self.position_servos[2] = int(valor)
        for i in range(3):
            self.label_position[i].config(text=self.text_label_position[i] + str(self.posicion_efector_final(self.position_servos)[i]))
            self.label_rotation[i].config(text=self.text_label_rotation[i] + str(self.rotacion_efector_final(self.position_servos)[i]))

    def barra_deslizante_servo4(self, valor):
        self.entry_text_servo[3].delete(0, tk.END)
        self.entry_text_servo[3].insert(0, str(valor))
        jointMovement.jointMovement(4, int(valor))
        self.position_servos[3] = int(valor)
        for i in range(3):
            self.label_position[i].config(text=self.text_label_position[i] + str(self.posicion_efector_final(self.position_servos)[i]))
            self.label_rotation[i].config(text=self.text_label_rotation[i] + str(self.rotacion_efector_final(self.position_servos)[i]))

    def barra_deslizante_servo5(self, valor):
        self.entry_text_servo[4].delete(0, tk.END)
        self.entry_text_servo[4].insert(0, str(valor))
        jointMovement.jointMovement(5, int(valor))
        self.position_servos[4] = int(valor)
        for i in range(3):
            self.label_position[i].config(text=self.text_label_position[i] + str(self.posicion_efector_final(self.position_servos)[i]))
            self.label_rotation[i].config(text=self.text_label_rotation[i] + str(self.rotacion_efector_final(self.position_servos)[i]))

    barra_deslizante_servos = {
    1: barra_deslizante_servo1,
    2: barra_deslizante_servo2,
    3: barra_deslizante_servo3,
    4: barra_deslizante_servo4,
    5: barra_deslizante_servo5,
    }


def main():
    ventana = tk.Tk()
    app = PhantomXPincherApp(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()