#!/user/bin/env

# script de python correspondiente a un nodo tipo Teleop_key

import rospy
import time
import math
import numpy as np
from std_msgs.msg import String
from dynamixel_workbench_msgs.srv import DynamixelCommand

home_Position = [2048,3072,2048,1024,2800]
object_Position = [2560,1940,1475,2720,2260]
tall_Position = [2048,2048,3072,2048,2800]
squatting_Position = [2048,3072,1050,2048,2800]

# Envia la informacion a los motores para el servidor
def jointMovement( id_num, value):  
    rospy.init_node('PhantomX_Movement')
    #jointCommand('', id_num, 'Goal_Velocity', 10, 0.1) 
    if id_num == 1:
        value *=-1
    if id_num == 3:
        value -= 90
    jointCommand('', id_num, 'Goal_Position', grados_a_bits(value), 0.1) 

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

#Convierten los grados a bits
def grados_a_bits(grados):
    offset = 2048  # Este es el offset para que 0 grados sea 2048 en bits
    if grados >= 0:
        bits = offset - int((grados / 180) * offset)
    else:
        bits = offset + int((-grados / 180) * offset)
    return bits

# Matriz de transformación homogenea del TCP
def mth_tcp(theta, d, a, alpha, offset):
    tcp = np.eye(4)
    for i in range(len(theta)):
        tcp = np.dot(tcp,matriz_DH(theta[i]+offset[i],d[i], a[i], alpha[i]))

    return tcp    



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

def main():
    for joint in range(len(home_Position)):
        jointMovement('', joint+1,'Goal_Position', home_Position[joint], 0.1)


        rospy.sleep(20)

    for joint in range(len(home_Position)):
        jointMovement('', joint+1,'Goal_Position', object_Position[joint], 0.1)
        rospy.sleep(20)


if __name__ == '__main__':
    try:
         #Testing our function
        main()
    except rospy.ROSInterruptException: pass