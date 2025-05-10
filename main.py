from controller import Robot, DistanceSensor, PositionSensor, Camera, GPS, Emitter, Lidar
import cv2
import numpy as np
import struct
import math
import random


# variabili generali o globali
timeStep = 32
max_velocity = 5.1
rotation_speed = 5.0
maxLidarDistance = 0.14


# creazione robot
robot = Robot()


# dichiarazione ruota sinistra e ruota destra
wheel_left = robot.getDevice("wheel2 motor")
wheel_right = robot.getDevice("wheel1 motor")


# settare la posizione della ruota sinistra e della ruota destra
wheel_left.setPosition(float("inf"))
wheel_right.setPosition(float("inf"))
wheel_right.setVelocity(0)
wheel_left.setVelocity(0)


# sensori di distanza frontale, destro e sinistro
distanceSensorRight = robot.getDevice("distance sensor1")
distanceSensorLeft = robot.getDevice("distance sensor2")
distanceSensorFront = robot.getDevice("distance sensor3")
distanceSensorRight.enable(timeStep)
distanceSensorLeft.enable(timeStep)
distanceSensorFront.enable(timeStep)


# camera
cameraRight = robot.getDevice("camera1")
cameraLeft = robot.getDevice("camera2")
cameraRight.enable(timeStep)
cameraLeft.enable(timeStep)


# inertial unit
inertialUnit = robot.getDevice("inertial_unit")
inertialUnit.enable(timeStep)


# sensore di colore
colourSensor = robot.getDevice("colour_sensor")
colourSensor.enable(timeStep)


# emitter e receiver
receiver = robot.getDevice("receiver")
emitter = robot.getDevice("emitter")
receiver.enable(timeStep)


# GPS
gps = robot.getDevice("gps")
gps.enable(timeStep)


# lidar
lidar = robot.getDevice("lidar")
lidar.enable(timeStep)


start = robot.getTime()


def forward():
    wheel_left.setVelocity(max_velocity)
    wheel_right.setVelocity(max_velocity)


def goBack():
    wheel_left.setVelocity(-max_velocity)
    wheel_right.setVelocity(-max_velocity)


def stopMotors():
    wheel_left.setVelocity(0)
    wheel_right.setVelocity(0)


def spinOnRight():
    wheel_left.setVelocity(rotation_speed)
    wheel_right.setVelocity(-rotation_speed)


def spinOnLeft():
    wheel_left.setVelocity(-rotation_speed)
    wheel_right.setVelocity(rotation_speed)


def getColour():
    image = colourSensor.getImage()
    r = colourSensor.imageGetRed(image, 1, 0, 0)
    g = colourSensor.imageGetGreen(image, 1, 0, 0)
    b = colourSensor.imageGetBlue(image, 1, 0, 0)
    # print("r: " + str(r) + " g: " + str(g) + " b: " + str(b))
    if 203 <= r <= 233 and 170 <= g <= 200 and 93 <= b <= 123:
        print("Brown")
        return "brown"
    if 0 <= r <= 30 and 0 <= g <= 30 and 0 <= b <= 30:
        print("Black")
        return "black"
    if 225 <= r <= 255 and 50 <= g <= 80 and 50 <= b <= 80:
        print("Red")
        return "red"
    if 20 <= r <= 50 and 225 <= g <= 255 and 20 <= b <= 50:
        print("Green")
        return "green"
    if 50 <= r <= 80 and 50 <= g <= 80 and 225 <= b <= 255:
        print("Blue")
        return "blue"
    if 113 <= r <= 173 and 56 <= g <= 79 and 225 <= b <= 255:
        print("Purple")
        return "purple"
    if 120 <= r <= 180 and 120 <= g <= 180 and 120 <= b <= 180:
        print("Gray")
        return "gray"
    if 29 <= r <= 59 and 33 <= g <= 63 and 46 <= b <= 76:
        print("Checkpoint")
        return "checkpoint"
    if 93 <= r <= 123 and 93 <= g <= 123 and 93 <= b <= 123:
        print("Hole border")
        return "hole"
    if 225 <= r <= 255 and 225 <= g <= 255 and 225 <= b <= 255:
        print("White")
        return "white"
    if 86 <= r <= 116 and 177 <= g <= 127 and 191 <= b <= 221:
        print("Wall")
        return "wall"
    if 42 <= r <= 46 and 42 <= g <= 46 and 42 <= b <= 46:
        print("Wall Black")
        return "wallB"
    if 126 <= r <= 234 and 222 <= g <= 255 and 231 <= b <= 255:
        print("Strange wall")
        return "wallS"


def getLidarDistanceFront():
    lidarArray = lidar.getRangeImage()
    avgDistance = 0.0
    rightValue = 0
    # print("-----------------------------------")
    for i in list(range(1023,1055)) + list(range(1503,1535)):
        if lidarArray[i] < maxLidarDistance:
            avgDistance += lidarArray[i]
            rightValue += 1
            # print(f"i {i-1023}: {round(lidarArray[i],3)} ")
    if rightValue <= 10:
        return 1.0
    avgDistance = round(avgDistance / rightValue,3)
    print(f"The average front distance is :  {avgDistance}")
    return avgDistance


def getLidarDistanceRight():
    lidarArray = lidar.getRangeImage()
    avgDistance = 0.0
    rightValue = 0
    # print("-----------------------------------")
    for i in range(1119,1183):
        if lidarArray[i] < maxLidarDistance:
            avgDistance += lidarArray[i]
            rightValue += 1
            # print(f"i {i-1023}: {round(lidarArray[i],3)} ")
    if rightValue <= 10:
        return 1.0
    avgDistance = round(avgDistance / rightValue, 3)
    print(f"The average right distance is :  {avgDistance}")
    return avgDistance


def getLidarDistanceBack():
    lidarArray = lidar.getRangeImage()
    avgDistance = 0.0
    rightValue = 0
    # print("-----------------------------------")
    for i in range(1247,1311):
        if lidarArray[i] < maxLidarDistance:
            avgDistance += lidarArray[i]
            rightValue += 1
            # print(f"i {i-1023}: {round(lidarArray[i],3)} ")
    if rightValue <= 10:
        return 1.0
    avgDistance = round(avgDistance / rightValue, 3)
    print(f"The average back distance is :  {avgDistance}")
    return avgDistance


def getLidarDistanceLeft():
    lidarArray = lidar.getRangeImage()
    avgDistance = 0.0
    rightValue = 0
    # print("-----------------------------------")
    for i in range(1375,1439):
        if lidarArray[i] < maxLidarDistance:
            avgDistance += lidarArray[i]
            rightValue += 1
            # print(f"i {i-1023}: {round(lidarArray[i],3)} ")
    if rightValue <= 10:
        return 1.0
    avgDistance = round(avgDistance / rightValue, 3)
    print(f"The average left distance is :  {avgDistance}")
    return avgDistance


def turnLeft():
    currentOrientation = inertialUnit.getRollPitchYaw()[2]
    targetOrientation = 0.0
    if -0.1 <= currentOrientation <= 0.1: # nord
        print("nord")
        targetOrientation = math.pi/2
        spinOnLeft()
    elif (math.pi/2 - 0.1) <= currentOrientation <= (math.pi/2 + 0.1): # ovest
        print("ovest")
        targetOrientation = math.pi
        spinOnLeft()
    elif -math.pi <= currentOrientation <= (-math.pi + 0.1) or (math.pi - 0.1) <= currentOrientation <= math.pi: # sud
        print("sud")
        targetOrientation = -(math.pi / 2)
        spinOnLeft()
    elif (-(math.pi/2) - 0.1) <= currentOrientation <= (-(math.pi/2) + 0.1): # est
        print("est")
        targetOrientation = 0.0
        spinOnLeft()
    while robot.step(timeStep) != -1:
        newCurrentOrientation = inertialUnit.getRollPitchYaw()[2]
        if abs(angleNormalization(newCurrentOrientation - targetOrientation)) < 0.05:
            stopMotors()
            print("Left turn completed")
            return


def turnRight():
    currentOrientation = inertialUnit.getRollPitchYaw()[2]
    targetOrientation = 0.0
    if -0.1 <= currentOrientation <= 0.1: # nord
        print("nord")
        targetOrientation = -(math.pi/2)
        spinOnRight()
    elif (-(math.pi/2) - 0.1) <= currentOrientation <= (-(math.pi/2) + 0.1): # est
        print("est")
        targetOrientation = math.pi
        spinOnRight()
    elif -math.pi <= currentOrientation <= (-math.pi + 0.1) or (math.pi - 0.1) <= currentOrientation <= math.pi: # sud
        print("sud")
        targetOrientation = math.pi/2
        spinOnRight()
    elif (math.pi/2 - 0.1) <= currentOrientation <= (math.pi/2 + 0.1): # ovest
        print("ovest")
        targetOrientation = 0.0
        spinOnRight()
    while robot.step(timeStep) != -1:
        newCurrentOrientation = inertialUnit.getRollPitchYaw()[2]
        if abs(angleNormalization(newCurrentOrientation - targetOrientation)) < 0.05:
            stopMotors()
            print("Turn turn completed")
            return


def angleNormalization(angle):
    return math.atan2(math.sin(angle),math.cos(angle))


def wallAhead():
    if getLidarDistanceLeft() > getLidarDistanceRight():
        turnLeft()
    elif getLidarDistanceLeft() < getLidarDistanceRight():
        turnRight()
    else:
        if random.randint(1, 100) % 2 == 0:
            turnLeft()
        else:
            turnRight()
            
            
# def directionCorrection():
#     currentOrientation = inertialUnit.getRollPitchYaw()[2]
#     targetOrientation = 0.0
#     if -math.pi/4 <= currentOrientation <= math.pi/4:
#         print("nord")
#         #spin
#         #targetOrientation = 0.0
#     elif math.pi/4 <= currentOrientation <= 3 * math.pi/4:
#         print("ovest")
#         #spin
#         #targetOrientation = math.pi/2
#     elif 3 * math.pi/4 <= currentOrientation <= math.pi or -math.pi <= currentOrientation <= - 3 * math.pi/4:
#         print("sud")
#         #spin
#         #targetOrientation = math.pi
#     elif - 3 * math.pi/4 <= currentOrientation <= - math.pi/4:
#         print("est")
#         #spin
#         #targetOrientation = -math.pi/2
#     while robot.step(timeStep) != -1:
#         newCurrentOrientation = inertialUnit.getRollPitchYaw()[2]
#         if abs(angleNormalization(newCurrentOrientation - targetOrientation)) < 0.05:
#             stopMotors()
#             print("direction correction completed")
#             return


def hole():
    goBack()
    while robot.step(timeStep) != -1:
        if getColour() == "white":
            break
    wallAhead()


def getImageCamera():
    image1 = cameraRight.getImage()
    image2 = cameraLeft.getImage()
    width = cameraRight.getWidth()
    height = cameraLeft.getHeight()
    image_array1 = np.frombuffer(image1, dtype=np.uint8).reshape((height, width, 4))
    image_array2 = np.frombuffer(image2, dtype=np.uint8).reshape((height, width, 4))
    image_rgb1 = cv2.cvtColor(image_array1, cv2.COLOR_RGBA2RGB)
    image_rgb2 = cv2.cvtColor(image_array2, cv2.COLOR_RGBA2RGB)
    image_resized1 = cv2.resize(image_rgb1, (64, 40))
    image_resized2 = cv2.resize(image_rgb2, (64, 40))
    cv2.imwrite("captured_image_cameraRight.jpg", image_resized1)
    cv2.imwrite("captured_image_cameraLeft.jpg", image_resized2)


def main():
    while robot.step(timeStep) != -1:
        getImageCamera()
        if getColour() == "hole":
            goBack()
        if getLidarDistanceFront() <= 0.065:
            stopMotors()
            if getLidarDistanceRight() <= 0.08:
                print("spin on left")
                turnLeft()
            elif getLidarDistanceLeft() <= 0.08:
                print("spin on right")
                turnRight()
            else:
                print("Wall ahead")
                wallAhead()
            continue
        forward()


if __name__ == "__main__":
    main()
