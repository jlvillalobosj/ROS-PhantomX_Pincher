# ROS-PhantomX_Pincher

# Grupo 2

- Julian Leonardo Villalobos Jiménez - jlvillalovbosj@unal.edu.co
- Jhonathann Alexander Gómez Velásquez - jhagomezve@unal.edu.co

El presente repositorio tiene por objetivo dar a conocer el funcionamiento del brazo robótico Phantom X Pincher basado en en movimientos otrogados por los motores Dynamixel los cuales son programados a partir de los paquetes de ROS.

<p align="center">
  <img src="/Imagenes/PhantomXGeneral.PNG" style="width: 45%; height: auto;" /  />
</p>

## Solución planteada

Para el desarrollo del diseño de una interfaz para la manipulación de un robot Dynamixel, fue necesario conocer inicialmente las diferentes características del robot. Por medio de la aplicación Dynamixel Wizard, se determinaron los IDs que correspondían a los servomotores del brazo robótico, los límites de las articulaciones en bits y las direcciones de nombres para las acciones que pueden manipular al robot. Luego, se procedió a utilizar comandos para crear un servicio desde un terminal, de esta forma se conocieron los requisitos necesarios para enviar y recibir respuestas en su nodo maestro.

En cuanto a la interfaz, se inició creando una pantalla de inicio en Python usando Visual Studio. Esta pantalla cuenta con un botón que permite iniciar el nodo maestro del proyecto Dynamixel y, con su ayuda, solicitar todos los requerimientos necesarios. En la ventana principal, se diseñaron cinco botones encargados de llamar a los servicios con los mismos requerimientos, pero con diferentes valores, permitiendo variar la posición de los servomotores a los deseados.

Para aumentar la interacción con la aplicación y el robot, se diseñaron cinco sliders y cinco campos de entrada que permiten al usuario manipular las posiciones que puede tomar el robot. Finalmente, se añadieron indicadores para mostrar la distancia y rotación del efector final respecto a la base, con el fin de proporcionar al usuario una descripción más detallada del estado en que se encuentra un objeto cuando es sujetado por el brazo robótico.

## Funciones de matlab

Inicialmente botenemos la matriz de Denavit-Hartenberg (DH) describe cómo cada articulación de un robot afecta su posición y orientación. Al definir la configuración DH para cada articulación, establecemos parámetros como el ángulo de rotación y la longitud del enlace. Multiplicando las matrices DH a lo largo del robot, obtenemos la matriz de transformación homogénea, que nos da la posición y orientación del extremo del robot. 
<p align="center">
  <img src="/Imagenes/DiagramaphantomX.PNG" style="width: 45%; height: auto;" /  />
  <img src="/Imagenes/MatrizDH.PNG" style="width: 45%; height: auto;" /  />
</p>

Para el diseño del código principal, se inició estableciendo las características que influyen en los movimientos del brazo robótico, tales como su espacio de trabajo con el fin de conocer los alcances que este tiene, por medio del vector L se indican las longitudes de cada eslabon en centímetros, por medio del vector q se representan los  ángulos que toma cada articulación en base a las variables de entrada dadas por el usuario al interactuar con la interfaz (botones, sliders, spinners), finalmente el plot_optiosn{} nos permite armar la base donde se verá la simulación del brazo robótico.
```matlab

            ws = [-24 24 -24 24 -4.5 40];
            L = [4.5, 10, 10, 1, 10]; 
            offset = [0, -pi/2, 0, -pi/2, 0];
            q = [app.valueServo1, app.valueServo2, app.valueServo3, app.valueServo4, app.valueServo5]*pi/180;
            limitesEjes = [-25 25; -25 25; -5 45];

            plot_options = {'workspace',ws,'scale',.5,'noa','view',[125 25], 'tilesize',2, ...
                            'ortho', 'lightpos',[2 2 10], ...
                            'floorlevel',0, 'base'};
```
A continuación se hace el diseño de cada uno de los parámetros de la matriz de Denavit-Hartenberg (DH) en donde se indican el tipo de articulación que son, sus respectivas propiedades de angulos y longitudes y los límites de desplazamiento que tienen para finalmente usar la funcion de SerialLink de PeterCorke para modelar, simular y analizar la cadena cinemática de nuestro robot y finalmente obtener su visualización.
```matlab
            
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
Seguidamente se diseño la gráfica del robot resultante por medio de la función .plot(), en donde se especificaban los angulos por medio del vector q y el espacio de trabajo. Ya que se espera que la gráfica se actualice con respecto a las interacciones del usuario es necesario eliminar la grafica anterior por lo que el codigo inicia con la funcion clf.
```matlab 
             clf;
             cla(app.UIAxes);
             ax = axes();
             RobotPhantomx.plot(q,'workspace',ws); 
             xlim([limitesEjes(1,:)])
             ylim([limitesEjes(2,:)])
             zlim([limitesEjes(3,:)])
             copyobj(ax.Children, app.UIAxes);
             grid(app.UIAxes, 'on');
             xlim(app.UIAxes, [limitesEjes(1,:)]); 
             ylim(app.UIAxes, [limitesEjes(2,:)]); 
             zlim(app.UIAxes, [limitesEjes(3,:)]);
```
Finalmente se calculó la matriz de transformación homogenea del TCP por medio de la funcion fkine() de peter corke con el fin de obtener la posición y la orientación en la que se encontraba el efector final y mostrarselos al usuario por medio de una etiqueta variable.
```matlab               
            TCP = RobotPhantomx.fkine(q)
            rotacion = tr2rpy(TCP,'zyx','deg')
            poscicion = TCP.T
            Posicion=poscicion(1:3, 4);               
            app.Roll.Value = round(rotacion(1), 2);             
            app.Pitch.Value = round(rotacion(2), 2);             
            app.Yaw.Value = round(rotacion(3), 2);   

            app.AlturaEditField.Value = round(Posicion(1), 2);             
            app.VerticalEditField.Value = round(Posicion(2), 2);             
            app.HorizontalEditField.Value = round(Posicion(3), 2);
```


En el siguiente [enlace](Matlab/Laboratorio4_PhantomX/appMovementPhantomX.mlapp) encuentra la aplicación para el funcionamiento de la interfaz del brazo robótico en matlab, por otro lado el código base de la aplicación donde se hace uso del .teach para la comparación de resultados lo puede encontrar en el siguiente [enlace](Matlab/Laboratorio4_PhantomX/CinematicaDirecta.m)


## Simulación de MATLAB
Se creó una interfaz en MATLAB para simular diversas posiciones del sistema utilizando la Toolbox de Robótica de Peter Corke. La interfaz permite visualizar tanto la posición como la orientación del efector final del brazo robótico. Además, se incorporaron barras de deslizamiento (sliders) para brindar mayor precisión en la selección de las posiciones deseadas del brazo robótico.
<p align="center">
  <img src="/Imagenes/InterfaceMatlab.PNG" style="width: 80%; height: auto;" /  />
</p>

## Interfaz gráfica
El diseño de la interface se dividio en dos partes, la primera se basa en una pequeña introducción a la aplicación en donde aparecen los nombres de los integrantes y un pequeño parrafo con la descripción de la aplicación. Al seleccionar el boton de "inicio", se evalua si el roslaunch esta en funcionamiento, con lo cual procede a cerrar la ventana actual y abrir la ventana principal donde se encuentran las diferentes acciones ue se pueden realizar para mover el robot.

<p align="center">
  <img src="/Imagenes/HomeApp.PNG" style="width: 45%; height: auto;" /  />
</p>

Por otro lado en la ventana principal encontramos inicialmente los botones principales que se encargan de colocar al robot en posiciones específicas en base a los ángulos de rotación de cada servomotor tales como:
-  [0, 0, 0, 0, 0] - Para la posición del Home
- [25, 25, 20, -20, 0] - Para la posición del objeto
- [-35,35, -30, 30, 0] - Para la posición 1
- [85, -20, 55, 25, 0] - Para la posición 2
- [80, -35, 55, -45, 0] - Para la posición 3

Al igual que en la simulación de matlab, los slider y las entras de texto junto con los botones estan conectados recíprocamente ya que al ejecutar una acción en cualquiera de estos, se mostrara el cambio en los demas, del mismo modo se implementaron 5 sliders para tener control sobre cada uno de los servomotores y tener un mayor control sobre el robot. Finalmente se implementaron unas ediciones de texto las cuales se encargan de mostrar la posición y orientación en la que se encuentra el efector final den base a su punto de apoyo estas calculadas por medio de la matriz DH y la matriz de transformación homogenea del TCP
<p align="center">
  <img src="/Imagenes/InterfacePython.PNG" style="width: 45%; height: auto;" /  />
</p>
Es importante aclarar que en caso de tener una entrada de texto que se encuentre fuera del limite de rotación en los servomotores se mostrara un mensaje de error indicando que esos valores no se encuentran dentro de los parámetros.

## Funciones de ROS

Una vez se hayan terminado los diferentes cambios para el funcionamiento de la aplicaci[on se inserta el comando *catkin build dynamixel_one_motor* con el fin de reconstruir y compilar el proyecto para revisar el correcto funcionamiento de los cambios realizados. Seguidamente se  *source devel/setup.bash* dentro de la carpeta del workspace con el fin de permitir a ROS reconocer y utilizar correctamente los paquetes y recursos del workspace para finalmente correr el comando *roslaunch dynamixel_one_motor one_controller.launch* el cual nos permite poner en marcha los nodos del proyecto de dynamixel motor y sar los servicios de este.

Mientras la aplicación se encuentra en ejecución, al seleccionar el botón de inicio el sistema busca el nodo master de la aplicación para dan permiso a los comandos para los tópicos, lo servicios y las acciones e inmediatemente destruye la ventana actual para dar paso al script de la interface de los movimientos del robot. En caso de no tener corriendo el proyecto de roslaunch la aplicación envia un mensaje de error por medio de una ventana modal.
<p align="center">
  <img src="/Imagenes/ErrorConexion.PNG" style="width: 45%; height: auto;" /  />
</p>

```python             
    def boton_push_start(self):
          # Intenta inicializar rospy y muestra un mensaje indicando el estado de la conexión
          try:
              rospy.init_node('PhantomX_Movement')
              self.screen.destroy()
              interface.main()
          except Exception:
              messagebox.showerror("Error de conexión", "No se pudo establecer la conexión con el Phantom X")
              pass
```
Al ejecutar alguna acción sobre el robot, ya sea por medio de los botones, los sliders o las entradas de texto, esta hara un llamado al servicio de ros (la aplicación esta configurada para que cuando se inicie la pantalla principal, la primera acion que se ejecute es colocar al robot en la posición HOME)
```python             
        #Ejecutar en la posición home solo al inicio
        for joint in range(len(self.home_Position)):
            jointMovement.jointMovement(joint+1,self.home_Position[joint])
```
La función jointMovement(id,value) es la primera función que se ejecuta cuando se solicita cualquier movimiento del robot, esta se encarga de ajustar los parámetros de entrada para los comandos del servicio, inicialmente en el servomotor 1 al presentar una orioentación invertida con respecto a los demas servomotores se implemento una negación a los valores de entrada, por otro lado para el servomotor 3 al presentar una inclinación de 90° en la estructura fué necesario restarle estos 90° a los diferentes valores que llegaran para este ID con el fin de tener los resultados acorde a los cálculos, y finalmente antes de hacer un llamado a la función delñ jointCommand se ejecuta la función grados_a_bits() el cual se encarga de convertir los datos entrados por el usuario a valores que puede entender el servomotor.

```python             
# Envia la informacion a los motores para el servidor
def jointMovement( id_num, value):  
    if id_num == 1:
        value *=-1
    if id_num == 3:
        value -= 90
    jointCommand('', id_num, 'Goal_Position', grados_a_bits(value), 0.1) 
```
Ya que la interpretación del servomotor es een un rango de bits de 0 1 4096, se buscaba que el usuario pudiera ingresar valores de -180 a +180 haciendo que el 0° sea la parte frontal del servomotor, por lo que se tomo el valor de desplazamiento por defecto en 2048 para el caso que la entrada fuera 0°, en caso que el valor en grados sea positivo el valor en bits disminuira haciendo que este gire en contra de las manesillas del reloj y transformadno el valor de grados a bits por medio de la expresion matemática (grados/180)*bits_offset, por otro lado al ingresar un valor en grados negativo el valor en bits aumentara causando que gire en la dirección contraria.
```python             
#Convierten los grados a bits
def grados_a_bits(grados):
    offset = 2048  # Este es el offset para que 0 grados sea 2048 en bits
    if grados >= 0:
        bits = offset - int((grados / 180) * offset)
    else:
        bits = offset + int((-grados / 180) * offset)
    return bits
```
Unavez ajustado los parámetros requeridos por el comando de dynamixel se procede a llamar la función jointCommand() la cual se utiliza para esperar a que el servicio llamado 'dynamixel_workbench/dynamixel_command' esté disponible antes de continuar ejecutando el código para que los demas procesos finalicen, una vez se tenga el espacio disponible se hace uso del comando de service por medio de la función rospy *rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)*, esta me permite crear un servicio y guardarlo en la variable dynamixel_command para ingresarle de este modo los requerimientos tales como el id, la dirección de acciones de dynamixel (En este caso se usa solo *'Goal_Position'* ya que queremos ubicar los servomotores en una posición de bits específica) y su respectivo valor en bits, se guarda esta información en la variable result y la respuesta de esta función es un booleano indicndo si el servicio se realizó satisfactoriamente.
```python             
#LLama al servicio de ROS
def jointCommand(command, id_num, addr_name, value, time):  
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:        
        dynamixel_command = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        result = dynamixel_command(command,id_num,addr_name,value)
        rospy.sleep(time)
        return result.comm_result
    except rospy.ServiceException as exc:
        print(str(exc))
```

Para el cálculo de la posición y orientación del efector final se hace uso del mismo método implementado en la simulación de matlab en la cual se calcula inicialmente la matriz de transformación homogenea de cada eslabón basados en los parámetros DH.
<p align="center">
  <img src="/Imagenes/mthMatrizDH.PNG" style="width: 70%; height: auto;" /  />
</p>

```python             
# Matriz Denavit-Hartemberg para cada union
def matriz_DH(theta, d, a, alpha):
    alpha = math.radians(alpha)
    th = math.radians(theta)
    M1= [math.cos(th), -math.sin(th)*math.cos(alpha), math.sin(th)*math.sin(alpha), a*math.cos(th)]
    for i in range(len(M1)):
        M1[i] = round(M1[i],2)
    M2=[math.sin(th), math.cos(th)*math.cos(alpha), -math.sin(alpha)*math.cos(th), math.sin(th)*a]
    for i in range(len(M2)):
        M2[i] = round(M2[i],2)
    M3=[0, math.sin(alpha), math.cos(alpha), d]
    for i in range(len(M3)):
        M3[i] = round(M3[i],2)

    return [M1,M2,M3, [0, 0, 0, 1]]
```
Con ayuda de cada una de las matrices para los eslabones se calculó la MTH completa de la base al TCP realizando un producto punto entre cada uno de los resultados obtenidos 

```python             
# Matriz de transformación homogenea del TCP
def mth_tcp(theta, d, a, alpha, offset):
    tcp = np.eye(4)
    for i in range(len(theta)):
        tcp = np.dot(tcp,matriz_DH(theta[i]+offset[i],d[i], a[i], alpha[i]))

    return tcp    
```

Finalmente para obtener la posición y orientación en cada uno de los puntos en los que se ubique el robot, se hace uso de la función *matriz_parametros_pincher(self, theta)* la cual ingresa los ángulos respectivos de caad articulación y esta corre las funciones anteriormente descritas retornando la MTH SE3.
```python             
    def matriz_parametros_pincher(self, theta):
        d = [4.5, 0, 0, 0, 11]
        a = [0, 10, 10, 0, 0]
        offset = [0, -90, 0, -90, 0]
        alpha = [-90, 0, 0, -90, 0]
        return jointMovement.mth_tcp(theta, d, a, alpha, offset)  
```

Para los datos de la posición fué necesario tomar únicamente los valores de la cuarta columna de la matriz MTH, mientras que para la orientación se hizo el proceso inverso de la matriz para obtener los ángulos fijos en base a su sistema de orientación SO3 con lo cual se calcularon con operaciones trigonométricas.
```python             
    def posicion_efector_final(self, theta):
        posicion = [fila[3] for fila in self.matriz_parametros_pincher(theta)[:3]]
        for i in range(len(posicion)):
            posicion[i] = round(posicion[i],2)
        return posicion 
```

```python             
    def rotacion_efector_final(self, theta):
        rotacion = self.matriz_parametros_pincher(theta)

        yaw = math.atan2(rotacion[2][1], rotacion[2][2])
        yaw = round(math.degrees(yaw),1)

        pitch = math.atan2(rotacion[2][0],math.sqrt((rotacion[2][1])**2 + (rotacion[2][2])**2) )
        pitch = round(math.degrees(pitch),1)

        roll = math.atan2(-rotacion[0][1], rotacion[0][0])
        roll = round(math.degrees(roll),1)

        return [roll, pitch, yaw] 
```

<p align="center">
  <img src="/Imagenes/MatrizInversa.PNG" style="width: 70%; height: auto;" /  />
</p>


## Videos de pruebas de funcionamiento

Simulación matlab


https://github.com/jlvillalobosj/ROS-PhantomX_Pincher/assets/57506705/46163c2b-d1d2-443a-8d6c-82503bcfea16


Prueba Real python

No nos entregaron el robot a tiempo para subir el video del sistema funcionando :'v

