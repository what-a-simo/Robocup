from controller import Robot, DistanceSensor, PositionSensor, Camera, GPS, Emitter
import math
import cv2
import numpy as np
import tensorflow as tf
import struct
import time
import random

# timeStep e velocità massima
timeStep = 32
maxVelocity = 5.1
rotation_speed = 5.0


# creazione robot
robot = Robot()


# dichiarazione ruota sinistra e ruota destra
wheelLeft = robot.getDevice("wheel2 motor")
wheelRight = robot.getDevice("wheel1 motor")


# settare la posizione della ruota sinistra e della ruota destra
wheelLeft.setPosition(float("inf"))
wheelRight.setPosition(float("inf"))
wheelRight.setVelocity(0)
wheelLeft.setVelocity(0)


# sensori di distanza frontale, destro e sinistro
distanceSensorRight = robot.getDevice("distance sensor1")
distanceSensorLeft = robot.getDevice("distance sensor2")
distanceSensorFront = robot.getDevice("distance sensor3")

distanceSensorRight.enable(timeStep)
distanceSensorLeft.enable(timeStep)
distanceSensorFront.enable(timeStep)


# Camera
camera1 = robot.getDevice("camera1")
camera2 = robot.getDevice("camera2")
camera1.enable(timeStep)
camera2.enable(timeStep)


# inertial unit
inertialUnit = robot.getDevice("inertial_unit")
inertialUnit.enable(timeStep)


# sensore di colore
colorSensor = robot.getDevice("colour_sensor")
colorSensor.enable(timeStep)


# emitter e receiver
receiver = robot.getDevice("receiver")
emitter = robot.getDevice("emitter")
receiver.enable(timeStep)


# GPS
gps = robot.getDevice("gps")
gps.enable(timeStep)


# load model
model = tf.keras.models.load_model("/Users/simone/Documents/RoboCup/Erebus-v24_1_0/player_controllers/AI/testModel.keras")


# mapping
map = np.array([[0]])


# output dei sensori di distanza
def numToBlock(num):
    if num > 0.7:
        return '▁'
    elif num > 0.6:
        return '▂'
    elif num > 0.5:
        return '▃'
    elif num > 0.4:
        return '▄'
    elif num > 0.3:
        return '▅'
    elif num > 0.2:
        return '▆'
    elif num > 0.1:
        return '▇'
    elif num > 0:
        return '█'


start = robot.getTime()


def forward():
    wheelLeft.setVelocity(maxVelocity)
    wheelRight.setVelocity(maxVelocity)


def goBack():
    wheelLeft.setVelocity(-maxVelocity)
    wheelRight.setVelocity(-maxVelocity)


def stopMotors():
    wheelLeft.setVelocity(0)
    wheelRight.setVelocity(0)


def spinOnRight():
    wheelLeft.setVelocity(rotation_speed)
    wheelRight.setVelocity(-rotation_speed)


def spinOnLeft():
    wheelLeft.setVelocity(-rotation_speed)
    wheelRight.setVelocity(rotation_speed)


def nearWall():
    while robot.step(timeStep) != -1:
        forward()
        if getColour() == "wallB" or getColour() == "wallS":
            nearWallBack()
            break


def nearWallBack():
    while robot.step(timeStep) != -1:
        goBack()
        if getColour() == "brown" or getColour() == "white" or getColour() == "green" or getColour() == "checkpoint" or getColour() == "purple" or getColour() == "red" or getColour() == "blue":
            break


def turnTooMuch():
    stopMotors()
    targetOrientation = 3.1
    spinOnLeft()
    while robot.step(timeStep) != -1:
        currentOrientation = inertialUnit.getRollPitchYaw()[2]
        if abs(currentOrientation - targetOrientation) < 0.05:
            break



def wallAhead():
    while robot.step(timeStep) != -1:
        nRandom = random.randint(1,100)
        stopMotors()
        if distanceSensorRight.getValue() <= 0.2:
            #print("wall on right")
            turnOnLeft2()
            break
        elif distanceSensorLeft.getValue() <= 0.2:
            #print("wall on left")
            turnOnRight2()
            break
        elif nRandom % 2 == 0:
            turnOnLeft2()
        else:
            turnOnRight2()


def turnOnLeft2():
    stopMotors()
    nearWall()
    currentOrientation = inertialUnit.getRollPitchYaw()[2]
    if -0.2 <= currentOrientation <= 0.2:  #ovest
        targetOrientation = 1.6
        spinOnLeft()
        while robot.step(timeStep) != -1:
            currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
            if abs(currentOrientation2 - targetOrientation) < 0.05:
                return
    elif -1.8 <= currentOrientation <= -1.4:  #nord
        targetOrientation = 0.0
        spinOnLeft()
        while robot.step(timeStep) != -1:
            currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
            if abs(currentOrientation2 - targetOrientation) < 0.05:
                return
    elif -3.2 <= currentOrientation <= -2.9 or 2.9 <= currentOrientation <= 3.2:  #est
        targetOrientation = -1.6
        spinOnLeft()
        while robot.step(timeStep) != -1:
            currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
            if abs(currentOrientation2 - targetOrientation) < 0.05:
                return
    elif 1.4 <= currentOrientation <= 1.8:  #sud
        targetOrientation = 3.2
        spinOnRight()
        counter = 0
        while robot.step(timeStep) != -1:
            counter = counter + 1
            currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
            if abs(currentOrientation2 - targetOrientation) < 0.05:
                return
            elif counter == 50:
                turnTooMuch()
                return
    return


def turnOnRight2():
    stopMotors()
    nearWall()
    currentOrientation = inertialUnit.getRollPitchYaw()[2]
    if -0.2 <= currentOrientation <= 0.2: #est
        stopMotors()
        targetOrientation = -1.6
        spinOnRight()
        while robot.step(timeStep) != -1:
            currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
            if abs(currentOrientation2 - targetOrientation) < 0.05:
                return
    if -1.8 <= currentOrientation <= -1.4: #sud
        stopMotors()
        targetOrientation = 3.2
        spinOnRight()
        counter = 0
        while robot.step(timeStep) != -1:
            counter = counter + 1
            currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
            if abs(currentOrientation2 - targetOrientation) < 0.05:
                return
            elif counter == 50:
                turnTooMuch()
                return
    if -3.2 <= currentOrientation <= -2.8 or 2.9 <= currentOrientation <= 3.2: #ovest
        stopMotors()
        targetOrientation = 1.6
        spinOnRight()
        while robot.step(timeStep) != -1:
            currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
            if abs(currentOrientation2 - targetOrientation) < 0.05:
                return
    if 1.4 <= currentOrientation <= 1.8: #nord
        targetOrientation = 0.0
        spinOnRight()
        while robot.step(timeStep) != -1:
            currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
            if abs(currentOrientation2 - targetOrientation) < 0.05:
                return
    return


def directionCorrection():
    currentOrientation = inertialUnit.getRollPitchYaw()[2]
    if 0.2 <= currentOrientation <= 1.4:
        if currentOrientation <= 0.8: #nord
            stopMotors()
            targetOrientation = 0.0
            spinOnLeft()
            while robot.step(timeStep) != -1:
                currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
                if abs(currentOrientation2 - targetOrientation) < 0.05:
                    return
        else: #ovest
            stopMotors()
            targetOrientation = 1.6
            spinOnLeft()
            while robot.step(timeStep) != -1:
                currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
                if abs(currentOrientation2 - targetOrientation) < 0.05:
                    return
    if 1.8 <= currentOrientation <= 2.9:
        if currentOrientation <= 2.2: #ovest
            stopMotors()
            targetOrientation = 1.6
            spinOnLeft()
            while robot.step(timeStep) != -1:
                currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
                if abs(currentOrientation2 - targetOrientation) < 0.05:
                    return
        else: #sud
            stopMotors()
            targetOrientation = 3.2
            spinOnLeft()
            counter = 0
            while robot.step(timeStep) != -1:
                counter = counter + 1
                currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
                if abs(currentOrientation2 - targetOrientation) < 0.05:
                    return
                elif counter == 50:
                    turnTooMuch()
                    return
    if -2.9 <= currentOrientation <= -1.8:
        if currentOrientation <= -2.2: #sud
            stopMotors()
            targetOrientation = 3.2
            spinOnLeft()
            counter = 0
            while robot.step(timeStep) != -1:
                counter = counter + 1
                currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
                if abs(currentOrientation2 - targetOrientation) < 0.05:
                    return
                elif counter == 50:
                    turnTooMuch()
                    return
        else: #est
            stopMotors()
            targetOrientation = -1.6
            spinOnLeft()
            while robot.step(timeStep) != -1:
                currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
                if abs(currentOrientation2 - targetOrientation) < 0.05:
                    return
    if -1.4 <= currentOrientation <= -0.2:
        if currentOrientation <= -0.8: #est
            stopMotors()
            targetOrientation = -1.6
            spinOnLeft()
            while robot.step(timeStep) != -1:
                currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
                if abs(currentOrientation2 - targetOrientation) < 0.05:
                    return
        else: #nord
            stopMotors()
            targetOrientation = 0.0
            spinOnLeft()
            while robot.step(timeStep) != -1:
                currentOrientation2 = inertialUnit.getRollPitchYaw()[2]
                if abs(currentOrientation2 - targetOrientation) < 0.05:
                    return
    return


def hole():
    goBack()
    while robot.step(timeStep) != -1:
        if getColour() == "white":
            break
    wallAhead()


def getGpsValues():
    position = gps.getValues()
    x = position[0] * 100
    y = position[2] * 100
    return x, y


def printGpsValues():
    x, y = getGpsValues()
    print("X: " + str(x) + " - Y: " + str(y))


def getCameraRecognitionResult(image):
    image = image / 255.0
    image = tf.expand_dims(image, axis=0)

    output = model.predict(image)
    predictedClass = np.argmax(output)
    match predictedClass:
        case 0:
            print("Is corrosive")
            # time.sleep(2)
            return "C"
        case 1:
            print("Is flammable")
            # time.sleep(2)
            return "F"
        case 2:
            print("Is an H")
            # time.sleep(2)
            return "H"
        case 3:
            print("Is a wall")
            # time.sleep(2)
            return "1"
        case 4:
            print("Is organic")
            # time.sleep(2)
            return "0"
        case 5:
            print("Is poison")
            # time.sleep(2)
            return "P"
        case 6:
            print("Is an S")
            # time.sleep(2)
            return "S"
        case 7:
            print("Is an U")
            # time.sleep(2)
            return "U"
        case _:
            print("Undefined")
            return "-"


def getImageCamera():
    image1 = camera1.getImage()
    image2 = camera2.getImage()

    width = camera1.getWidth()
    height = camera1.getHeight()
    #print(str(width) + " " + str(height))

    imageArray1 = np.frombuffer(image1, dtype=np.uint8).reshape((height, width, 4))

    imageArray2 = np.frombuffer(image2, dtype=np.uint8).reshape((height, width, 4))

    image1 = cv2.cvtColor(imageArray1, cv2.COLOR_RGBA2RGB)
    image2 = cv2.cvtColor(imageArray2, cv2.COLOR_RGBA2RGB)
    cv2.imwrite("captured_image_camera1.jpg", image1)
    cv2.imwrite("captured_image_camera2.jpg", image2)

    imageResized1 = tf.io.read_file("captured_image_camera1.jpg")
    imageResized1 = tf.image.decode_jpeg(imageResized1, channels=3)
    imageResized1 = tf.image.resize(imageResized1,[64,40])

    imageResized2 = tf.io.read_file("captured_image_camera2.jpg")
    imageResized2 = tf.image.decode_jpeg(imageResized2, channels=3)
    imageResized2 = tf.image.resize(imageResized2, [64, 40])

    ch = getCameraRecognitionResult(imageResized1)
    #print(ch)
    if ch != "-" and ch != "1":
        stopMotors()
        #print("is in if")
        score(ch)
    ch = getCameraRecognitionResult(imageResized2)
    #print(ch)
    if ch != "-" and ch != "1":
        stopMotors()
        #print("is in if")
        score(ch)



def score(ch):
    stopMotors()
    victimType = bytes(ch, "utf-8")
    position = getGpsValues()
    x = int(position[0])
    y = int(position[1])
    message = struct.pack("i i c", x, y, victimType)
    emitter.send(message)


def getScore():
    message = struct.pack('c', 'G'.encode())
    emitter.send(message)
    if receiver.getQueueLength() > 0:
        receivedData = receiver.getBytes()
        tup = struct.unpack('c f i', receivedData)
        if tup[0].decode("utf-8") == 'G':
            #if int(tup[2]) == 5:
            #    emitter.send(bytes('E', "utf-8"))
            print(f'Game Score: {tup[1]}  Remaining time: {tup[2]}')
            receiver.nextPacket()


def navigate():
    while robot.step(timeStep) != -1:
        print(numToBlock(distanceSensorLeft.getValue()), numToBlock(distanceSensorFront.getValue()), numToBlock(distanceSensorRight.getValue()))
        print(round(inertialUnit.getRollPitchYaw()[2], 1))
        #printGpsValues()
        getColour()
        getImageCamera()
        #getScore()
        directionCorrection()
        if getColour() == "hole":
            stopMotors()
            hole()
        if distanceSensorFront.getValue() <= 0.2:
            stopMotors()
            if distanceSensorRight.getValue() <= 0.1:
                print("wall on right")
                turnOnLeft2()
            elif distanceSensorLeft.getValue() <= 0.1:
                print("wall on left")
                turnOnRight2()
            else:
                print("wall ahead")
                wallAhead()
        forward()


def getColour():
    image = colorSensor.getImage()
    r = colorSensor.imageGetRed(image, 1, 0, 0)
    g = colorSensor.imageGetGreen(image, 1, 0, 0)
    b = colorSensor.imageGetBlue(image, 1, 0, 0)
    #print("r: " + str(r) + " g: " + str(g) + " b: " + str(b))
    if 203 <= r <= 233 and 170 <= g <= 200 and 93 <= b <= 123:
        #print("Brown")
        return "brown"
    if 0 <= r <= 30 and 0 <= g <= 30 and 0 <= b <= 30:
        #print("Black")
        return "black"
    if 225 <= r <= 255 and 50 <= g <= 80 and 50 <= b <= 80:
        #print("Red")
        return "red"
    if 20 <= r <= 50 and 225 <= g <= 255 and 20 <= b <= 50:
        #print("Green")
        return "green"
    if 50 <= r <= 80 and 50 <= g <= 80 and 225 <= b <= 255:
        #print("Blue")
        return "blue"
    if 113 <= r <= 173 and 56 <= g <= 79 and 225 <= b <= 255:
        #print("Purple")
        return "purple"
    if 120 <= r <= 180 and 120 <= g <= 180 and 120 <= b <= 180:
        #print("Gray")
        return "gray"
    if 29 <= r <= 59 and 33 <= g <= 63 and 46 <= b <= 76:
        #print("Checkpoint")
        return "checkpoint"
    if 93 <= r <= 123 and 93 <= g <= 123 and 93 <= b <= 123:
        #print("Hole border")
        return "hole"
    if 225 <= r <= 255 and 225 <= g <= 255 and 225 <= b <= 255:
        #print("White")
        return "white"
    if 86 <= r <= 116 and 177 <= g <= 127 and 191 <= b <= 221:
        #print("Wall")
        return "wall"
    if 42 <= r <= 46 and 42 <= g <= 46 and 42 <= b <= 46:
        #print("Wall Black")
        return  "wallB"
    if 126 <= r <= 234 and 222 <= g <= 255 and 231 <= b <= 255:
        #print("Strange wall")
        return  "wallS"
    #height = colorSensor.getHeight()
    #width = colorSensor.getWidth()


# main
def main():
    while robot.step(timeStep) != -1:
        navigate()


if __name__ == "__main__":
    main()
