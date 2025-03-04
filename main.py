from controller import Robot, DistanceSensor, PositionSensor, Camera
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


def turnOnLeft():
    initial_orientation = inertialUnit.getRollPitchYaw()[2]
    target_orientation = initial_orientation - math.radians(-90)
    spinOnLeft()
    while robot.step(timeStep) != -1:
        current_orientation = inertialUnit.getRollPitchYaw()[2]
        if abs(current_orientation - target_orientation) < 0.05:
            break
    stopMotors()


def turnOnRight():
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


def navigate():
    while robot.step(timeStep) != -1:
        print(numToBlock(distanceSensorLeft.getValue()), numToBlock(distanceSensorFront.getValue()), numToBlock(distanceSensorRight.getValue()))
        print(round(inertialUnit.getRollPitchYaw()[2], 1))
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
    if r >= 203 and r <= 233 and g >= 170 and g <= 200 and b >= 93 and b <= 123:
        print("Brown")
        return "brown"
    if r >= 0 and r <= 30 and g >= 0 and g <= 30 and b >= 0 and b <= 30:
        print("Black")
        return "black"
    if r >= 225 and r <= 255 and g >= 0 and g <= 30 and b >= 0 and b <= 30:
        print("Red")
        return "black"
    if r >= 0 and r <= 30 and g >= 225 and g <= 255 and b >= 0 and b <= 30:
        print("Green")
        return "green"
    if r >= 0 and r <= 30 and g >= 0 and g <= 30 and b >= 225 and b <= 255:
        print("Blue")
        return "blue"
    if r >= 113 and r <= 173 and g >= 0 and g <= 30 and b >= 225 and b <= 255:
        print("Purple")
        return "purple"
    if r >= 120 and r <= 180 and g >= 120 and g <= 180 and b >= 120 and b <= 180:
        print("Gray")
        return "gray"
    if r >= 29 and r <= 59 and g >= 33 and g <= 63 and b >= 46 and b <= 76:
        print("Checkpoint")
        return "checkpoint"
    if r >= 93 and r <= 123 and g >= 93 and g <= 123 and b >= 93 and b <= 123:
        print("Hole border")
        return "hole"
    if r >= 225 and r <= 255 and g >= 225 and g <= 255 and b >= 225 and b <= 255:
        print("White")
        return "white"
    #height = colorSensor.getHeight()
    #width = colorSensor.getWidth()


# main
def main():
    while robot.step(timeStep) != -1:
        navigate()


if __name__ == "__main__":
    main()
