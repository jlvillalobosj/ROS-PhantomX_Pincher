# ROS-PhantomX_Pincher

# Grupo 2

- Julian Leonardo Villalobos Jiménez - jlvillalovbosj@unal.edu.co
- Jhonathann Alexander Gómez Velásquez - jhagomezve@unal.edu.co

El presente repositorio tiene por objetivo dar a conocer el funcionamiento del brazo robótico Phantom X Pincher basado en en movimientos otrogados por los motores Dynamixel los cuales son programados a partir de los paquetes de ROS.

<p align="center">
  <img src="/Imagenes/PhantomXGeneral.PNG" style="width: 45%; height: auto;" /  />
</p>

## Solucion planteada

## Funciones de MATLAB
Inicialmente botenemos la matriz de Denavit-Hartenberg (DH) describe cómo cada articulación de un robot afecta su posición y orientación. Al definir la configuración DH para cada articulación, establecemos parámetros como el ángulo de rotación y la longitud del enlace. Multiplicando las matrices DH a lo largo del robot, obtenemos la matriz de transformación homogénea, que nos da la posición y orientación del extremo del robot. 
<p align="center">
  <img src="/Imagenes/DiagramaphantomX.PNG" style="width: 45%; height: auto;" /  />
  <img src="/Imagenes/MatrizDH.PNG" style="width: 45%; height: auto;" /  />
</p>

## Diagrama de flujo

## Interfaz gráfica
El diseño de la interface se dividio en dos partes, la primera se basa en una pequeña introducción a la aplicación en donde aparecen los nombres de los integrantes y un pequeño parrafo con la descripción de la aplicación. Al seleccionar el boton de "inicio", se evalua si el roslaunch esta en funcionamiento, con lo cual procede a cerrar la ventana actual y abrir la ventana principal donde se encuentran las diferentes acciones ue se pueden realizar para mover el robot.

<p align="center">
  <img src="/Imagenes/HomeApp.PNG" style="width: 45%; height: auto;" /  />
</p>

Por otro lado en la ventana principal encontramos...
## Funciones de ROS

## DYNAMIXEL



## [Código main EPSON](/Lab2/Main.prg)




## Videos de pruebas de funcionamiento

Simulación

https://github.com/jlvillalobosj/Robot_EPSON/assets/57506705/6cfeb508-4afe-40cf-9301-b48298c972de

Prueba Real

https://github.com/jlvillalobosj/Robot_EPSON/assets/57506705/5ce8e1dd-460b-4427-b27b-d27af2a8e11b
