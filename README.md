# ROS-PhantomX_Pincher

# Grupo 2

- Julian Leonardo Villalobos Jiménez - jlvillalovbosj@unal.edu.co
- Jhonathann Alexander Gómez Velásquez - jhagomezve@unal.edu.co

El presente repositorio tiene por objetivo dar a conocer el funcionamiento del brazo robótico Robot VT6L de la marca EPSON, en donde por medio de funciones y comandos que nos permitiran otorgarle movimientos deseados y precisos al robot se realicen actividades de un entorno industrial.

<p align="center">
  <img src="/Imágenes/Robot_VT6L.PNG" style="width: 45%; height: auto;" /  />
 <img src="/Imágenes/Robot_VT6L_Sim.PNG" style="width: 30%; height: auto;" / />
</p>

## Solucion planteada

Para abordar el problema, se implementó la siguiente estrategia:

- Se estableció la conexión con el controlador del robot.
- Se fijó la posición HOME del robot, desde donde se iniciarán las trayectorias.
- Se identificaron los tres puntos esenciales para llevar a cabo el paletizado.
- Se desarrollaron las tres rutinas de paletizado requeridas.
- Se integraron las entradas y salidas para gestionar el flujo del programa y visualizar su estado.

## Diagrama de flujo

El diagrama de flujo presentado se basa en las acciones seriales del brazo robótico con las respectivas restricciones o condiciones que se consideran necesarias para el propósito del robot con diferentes funciones que son accesibles por entrada de datos externos

<p align="center">
  <img src="/Imágenes/Epson_Main.png" width="400" />
</p>
Desde el diagramma main del proyecto sehace el llamado a las diferentes funciones del robot, de modo que realice movimientos consecutivos: Al llamar al paletizado S, el sistema hace un recorrido por nuevec puntos realizado en fomra de S, al llamar el paletizado Z, realiza los movimientos de la matriz en forma de Z y finalmente al llamar la función Externa, realiza movimientos en forma de Z extraponiendo los valores de la matriz original.
<p align="center">
  <img src="/Imágenes/Diagrama_FuncionPaletizadoZ.PNG" style="width: 45%; height: auto;" /  />
 <img src="/Imágenes/PaletizadoZ.PNG" style="width: 45%; height: auto;" / />
</p>

<p align="center">
  <img src="/Imágenes/Paletizado_Externo.PNG" width="400" />
</p>

## Funciones utilizadas

Con ayuda del manual de epson [[Guia_Manual](/GuiasEPSON/epson_spel_pl_70_language_reference-r700a_rc90_t(v73r4).pdf)] se usaron diferentes funciones internas de EPSON para el diseño de las trayectorias.

1. Funciones de configuración
    - *Motor On,Off:* Activa o desactiva la salida de los motores del brazo robótico.
    - *Power HIGH; LOW:* Establece los niveles de potencia con los que se van a alimentar los motores del brazo robótico para de este modo no forzar las diferentes movimientos.
    - *Speed:* Indica a nivel portentual la velocidad máxima que van a tener los motores durante cada desplazamiento.
    - *Accel:* Indica el nivel de aceleración y desaceleración en los motores para llegar a su velocidad máxima y mínima.
2. Funciones de desplazamiento
    - *Go:* Desplaza el robot a un punto realizando un movimiento puntual, es necesario en este caso mencionar el movimieintomen Z para desplazarlo verticalmente como una función aparte, se aclara que por medio de este movimiento el robot sufre menos esfuerzos por lo que es menos posible que aparezcan errores en este caso.
    - *Move:* Desplaza el robot hasta el punto referenciado usando una interpolación lineal, aunque usa un trayecto mas corto puede afectar alguna de las articulaciones del robot
    - *Wait:* Se encarga de pausar la ejecución del código hasta cumplir una condición específica, ya sea por alguna señal de entrada, un tiempo determinado, entre otras.
    - *Call:* Se considera como un llamado a una función externa a la que se este realizando.
3. Funciones de entradas y salidas
    - *MemSw():* Entrada binaria desde memoria, tomando valores desde el 512
    - *MemOn():* Salida binaria desde memoria, tomando valores desde el 512
4. Pallet()
    - Se encarga de diseñar una matriz plana la cual nos facilita recorrerla bajo coordenadas específicas y precisas
    - El Pallet externo se encarga de formar una columna o una fila adicional a la que se crea por defecto, tambien nos evita el diseño de un ciclo anidado lo que vuelve el sistema mas lento.

## [Código main EPSON](/Lab2/Main.prg)

Para el diseño del código se inició crando un punto nombrado como HOME, desde el cual el robot parte para iniciar las trayectorias. Seguido a esto se crean puntos para el origen, el EjeX y el EjeY, los cuales nos ayudan para referenciar los mapeos que se realizan durante las trayectorias.

<p align="center">
  <img src="/Imágenes/CreacionHerramienta.PNG" />
 <img src="/Imágenes/Puntos_X_Y_Origen.PNG" style="width: 45%; height: auto;" />
</p>

A continuación se crearon los diferentes nombres como referencia para cada una de las salidas, desde la función main se activaron los motores y se establecio una salida de potencia alta en cada uno de estos, una vez pasados por los puntos del estado HOME, se procedió a pasar por los puntos creados de "Origen", "EjeX" y "EjeY", con el fin de evaluar los mapeos que se van a crear atraves de estosl.

<p align="center">
  <img src="/Imágenes/Codigo_TrayectoriaHOME.PNG" />
</p>

Se creó la función paletizado Z el cual consiste en realizar una trayectorias en forma de Z atraves de una matriz diseñada de 3x3 y que llegue a los puntos de origen, del eje x y del eje Y, para esto se diseñó una función ciclica por el cual pasara por todos los puntos del Pallet del 1 al 9.

<p align="center">
  <img src="/Imágenes/Codigo_FuncionPaletizadoZ.PNG" />
</p>

Se creó la función paletizado S el cual consiste en realizar una trayectorias en forma de S através de una matriz diseñada de 3x3 y que llegue a los puntos de origen, del eje x y del eje Y, para esto se paso como una secuencia normal de los 9 puntos con una funcion ciclica, al llegar al punto 4, esta pasa inmediatamente a la posición 6, mientras que cuando llegue al punto 6 esta debe pasar por la posición 4, el resto de las posiciones si conservan sus mismos puntos.

<p align="center">
  <img src="/Imágenes/Codigo_FuncionPaletizadoS.PNG" />
</p>

Se creó la función paletizado externo la cual consiste en el diseño deun pallet através de una matriz 4x4 y que pase por los 16 puntos entre los cuales se encuentran las posiciones de "Origen", del "EjeX" y del "EjeY" por medio de una fuinción ciclica de 16 posiciones.

<p align="center">
  <img src="/Imágenes/Codigo_FuncionPaletizadoExterno.PNG" />
</p>

Finalmente se diseño en la función main un ciclo el cual leyera cada una de las entradas, al tener una señal de entrada en el bit 512, el sistema activara la salida del bit 515 y llamara la función del paletizado Z, por otro lado al activar la entrada del bit 513 este llamara la función del paletizado en S activando la salida del biot 516, y finalmente con la señal de entrada del bit 514 se llamara la funcion del paletizado externo activando del mismo modo la salida del bit 517.

<p align="center">
  <img src="/Imágenes/Codigo_CicloTrayectorias.PNG" />
</p>

Para acceder al código puede seleccionar el subtítuo de esta sección "Código main EPSON" o darle clic [aquí](/Lab2/Main.prg)

## Videos de pruebas de funcionamiento

Simulación

https://github.com/jlvillalobosj/Robot_EPSON/assets/57506705/6cfeb508-4afe-40cf-9301-b48298c972de

Prueba Real

https://github.com/jlvillalobosj/Robot_EPSON/assets/57506705/5ce8e1dd-460b-4427-b27b-d27af2a8e11b
