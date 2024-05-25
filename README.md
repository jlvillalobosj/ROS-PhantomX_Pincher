# ROS-PhantomX_Pincher

# Grupo 2

- Julian Leonardo Villalobos Jiménez - jlvillalovbosj@unal.edu.co
- Jhonathann Alexander Gómez Velásquez - jhagomezve@unal.edu.co

El presente repositorio tiene por objetivo dar a conocer el funcionamiento del brazo robótico Phantom X Pincher basado en en movimientos otrogados por los motores Dynamixel los cuales son programados a partir de los paquetes de ROS.

<p align="center">
  <img src="/Imagenes/PhantomXGeneral.PNG" style="width: 45%; height: auto;" /  />
</p>

## Solucion planteada

## [Funciones de MATLAB](/Lab2/Main.prg)
Inicialmente botenemos la matriz de Denavit-Hartenberg (DH) describe cómo cada articulación de un robot afecta su posición y orientación. Al definir la configuración DH para cada articulación, establecemos parámetros como el ángulo de rotación y la longitud del enlace. Multiplicando las matrices DH a lo largo del robot, obtenemos la matriz de transformación homogénea, que nos da la posición y orientación del extremo del robot. 
<p align="center">
  <img src="/Imagenes/DiagramaphantomX.PNG" style="width: 45%; height: auto;" /  />
  <img src="/Imagenes/MatrizDH.PNG" style="width: 45%; height: auto;" /  />
</p>

Para el diseño del código principal, se inició
```matlab
% Tu código aquí
ws = [-24 24 -24 24 -4.5 40];
            L = [4.5, 10, 10, 1, 10]; 
            offset = [0, -pi/2, 0, -pi/2, 0];
            q = [app.valueServo1, app.valueServo2, app.valueServo3, app.valueServo4, app.valueServo5]*pi/180;
            limitesEjes = [-25 25; -25 25; -5 45];

            plot_options = {'workspace',ws,'scale',.5,'noa','view',[125 25], 'tilesize',2, ...
                            'ortho', 'lightpos',[2 2 10], ...
                            'floorlevel',0, 'base'};
            
            %            Theta  d   a   alpha  type mdh offset  qlim
            ParameterDH(1) = Link('revolute'   ,'alpha',      -pi/2,  'a',  0,      'd', ...
                        L(1) , 'offset',    offset(1), 'qlim', [-0 2*pi]);
            
            ParameterDH(2) = Link('revolute'   ,'alpha',      0,  'a',  L(2),      'd', ...
                        0 , 'offset',    offset(2), 'qlim', [-pi/3 pi/3]);
            
            ParameterDH(3) = Link('revolute'   ,'alpha',      0,  'a',  L(3),      'd', ...
                        0 , 'offset',    offset(3), 'qlim', [-pi/2 pi/2]);
            
            ParameterDH(4) = Link('revolute'   ,'alpha',      -pi/2,  'a',  0,      'd', ...
                        0 , 'offset',    offset(4), 'qlim', [-2*pi/3 2*pi/3]);
            
            ParameterDH(5) = Link('revolute'   ,'alpha',      0,  'a',  0,      'd', ...
                        L(4)+L(5) , 'offset',    offset(5), 'qlim', [-2*pi/3 2*pi/3]);
            
            RobotPhantomx = SerialLink(ParameterDH,'name','PhantomX','plotopt',plot_options);
```
En el siguiente [enlace](Matlab/Laboratorio4_PhantomX/appMovementPhantomX.mlapp) encuentra la aplicación para el funcionamiento de la interfaz del brazo robótico en matlab
## Simulación de MATLAB
Se creó una interfaz en MATLAB para simular diversas posiciones del sistema utilizando la Toolbox de Robótica de Peter Corke. La interfaz permite visualizar tanto la posición como la orientación del efector final del brazo robótico. Además, se incorporaron barras de deslizamiento (sliders) para brindar mayor precisión en la selección de las posiciones deseadas del brazo robótico.
<p align="center">
  <img src="/Imagenes/InterfaceMatlab.PNG" style="width: 45%; height: auto;" /  />
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
