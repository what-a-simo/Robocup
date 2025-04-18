from controller import Robot, DistanceSensor, PositionSensor, Camera, GPS, Emitter, Lidar
import struct
import math

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

# Camera
cameraRight = robot.getDevice("camera1")
camera2 = robot.getDevice("camera2")
cameraRight.enable(timeStep)
camera2.enable(timeStep)

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
    # height = colorSensor.getHeight()
    # width = colorSensor.getWidth()


# def getPP(withRot=False):  # da mettere apposto
#     global rLidar
#     if rLidar == None:
#         rLidar = lidar.getRangeImage()
#     pp = []
#     ppRot = []
#     for i in range(2 * int(len(rLidar) / 4), 3 * int(len(rLidar) / 4)):  # [0,511]:
#         if rLidar[i] < maxDisLidar:
#             rot = ((i) / (len(rLidar) / 4)) * math.tau - verticalRotation
#             pp.append(V2(-math.sin(rot) * rLidar[i], -math.cos(rot) * rLidar[i]))
#             ppRot.append(-rot - (math.pi / 2))
#     if withRot:
#         return [pp, ppRot]
#     else:
#         return pp


def getlidarDistance():
    rangeImage = lidar.getRangeImage()
    for i in range(2 * int(len(rangeImage) / 4), 3 * int(len(rangeImage) / 4)):
        if rangeImage[i] < maxLidarDistance and (1023 <= i <= 1033 or 1525 <= i <= 1535):
            print("i " + str(i - 1024) + ": " + str(round(rangeImage[i], 3)) + " ", end='')


# main
def main():
    while robot.step(timeStep) != -1:
        lidarArray = lidar.getRangeImage()
        avgDistance = 0.0
        print("-----------------------------------")
        for i in list(range(1023,1038)) + list(range(1520,1535)):
            if lidarArray[i] < maxLidarDistance:
                avgDistance += lidarArray[i]
                print(f"i {i-1023}: {round(lidarArray[i],3)} ")
        avgDistance /= 30
        print(f"The average distance is :  {round(avgDistance,3)}")

if __name__ == "__main__":
    main()
