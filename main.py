
from controller import Robot, DistanceSensor, PositionSensor, Camera, GPS
import math


# timeStep e velocità massima
timeStep = 32
max_velocity = 5.1
rotation_speed = 5.0


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


# inertial unit
inertialUnit = robot.getDevice("inertial_unit")
inertialUnit.enable(timeStep)


# sensore di colore
colorSensor = robot.getDevice("colour_sensor")
colorSensor.enable(timeStep)


# GPS
gps = robot.getDevice("gps")
gps.enable(timeStep)


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


def nearWall():
    while robot.step(timeStep) != -1:
        forward()
        if getColour() == "wallB" or getColour() == "wallS":
            nearWallBack()
            break


def nearWallBack():
    while robot.step(timeStep) != -1:
        goBack()
        if getColour() == "brown" or getColour() == "white":
            break


def turnOnLeft():
    nearWall()
    initial_orientation = inertialUnit.getRollPitchYaw()[2]
    target_orientation = initial_orientation - math.radians(-90)
    spinOnLeft()
    while robot.step(timeStep) != -1:
        current_orientation = inertialUnit.getRollPitchYaw()[2]
        if abs(current_orientation - target_orientation) < 0.05:
            break
    stopMotors()


def turnOnRight():
    nearWall()
    initial_orientation = inertialUnit.getRollPitchYaw()[2]
    target_orientation = initial_orientation - math.radians(90)
    spinOnRight()
    while robot.step(timeStep) != -1:
        current_orientation = inertialUnit.getRollPitchYaw()[2]
        if abs(current_orientation - target_orientation) < 0.05:
            break
    stopMotors()


def wallAhead():
    while robot.step(timeStep) != -1:
        stopMotors()
        if distanceSensorRight.getValue() <= 0.8:
            print("wall on right")
            turnOnLeft()
            break
        elif distanceSensorLeft.getValue() <= 0.8:
            print("wall on left")
            turnOnRight()
            break
        else:
            turnOnLeft()
            break


def hole():
    while robot.step(timeStep) != -1:
        goBack()
        if getColour() == "white":
            break
    wallAhead()


def stayedForTooLong():
    forward()


def gpsValues():
    position = gps.getValues()
    x = position[0] * 100
    y = position[2] * 100
    return x, y


def printGpsValues():
    x, y = gpsValues()
    print("X: " + str(x) + " - Y: " + str(y))


def navigate():
    while robot.step(timeStep) != -1:
        print(numToBlock(distanceSensorLeft.getValue()), numToBlock(distanceSensorFront.getValue()), numToBlock(distanceSensorRight.getValue()))
        print(round(inertialUnit.getRollPitchYaw()[2], 1))
        printGpsValues()
        getColour()
        if getColour() == "hole":
            stopMotors()
            hole()
        if distanceSensorFront.getValue() <= 0.1:
            stopMotors()
            if distanceSensorRight.getValue() <= 0.2:
                print("wall on right")
                turnOnLeft()
            elif distanceSensorLeft.getValue() <= 0.2:
                print("wall on left")
                turnOnRight()
            else:
                print("wall ahead")
                wallAhead()
        forward()


def getColour():
    image = colorSensor.getImage()
    r = colorSensor.imageGetRed(image, 1, 0, 0)
    g = colorSensor.imageGetGreen(image, 1, 0, 0)
    b = colorSensor.imageGetBlue(image, 1, 0, 0)
    print("r: " + str(r) + " g: " + str(g) + " b: " + str(b))
    if 203 <= r <= 233 and 170 <= g <= 200 and 93 <= b <= 123:
        print("Brown")
        return "brown"
    if 0 <= r <= 30 and 0 <= g <= 30 and 0 <= b <= 30:
        print("Black")
        return "black"
    if 225 <= r <= 255 and 0 <= g <= 30 and 0 <= b <= 30:
        print("Red")
        return "black"
    if 0 <= r <= 30 and 225 <= g <= 255 and 0 <= b <= 30:
        print("Green")
        return "green"
    if 0 <= r <= 30 and 0 <= g <= 30 and 225 <= b <= 255:
        print("Blue")
        return "blue"
    if 113 <= r <= 173 and 0 <= g <= 30 and 225 <= b <= 255:
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
        return  "wallB"
    if 126 <= r <= 234 and 222 <= g <= 255 and 231 <= b <= 255:
        print("Strange wall")
        return  "wallS"
    #height = colorSensor.getHeight()
    #width = colorSensor.getWidth()


# main
def main():
    while robot.step(timeStep) != -1:
        navigate()


if __name__ == "__main__":
    main()
