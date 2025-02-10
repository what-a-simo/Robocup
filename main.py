from controller import Robot, DistanceSensor, PositionSensor

# timeStep e velocità massima
timeStep = 32
max_velocity = 5.1

# creazione robot
robot = Robot()

# dichiarazione ruota sinistra e ruota destra
wheel_left = robot.getDevice("wheel2 motor")
wheel_right = robot.getDevice("wheel1 motor")

# settare la posizione della ruota sinistra e della ruota destra
wheel_left.setPosition(float("inf"))
wheel_right.setPosition(float("inf"))

# encoder?
leftEncoder = wheel_left.getPositionSensor()
rightEncoder = wheel_right.getPositionSensor()

leftEncoder.enable(timeStep)
rightEncoder.enable(timeStep)

# sensori di distanza frontale, destro e sinistro
distanceSensorRight = robot.getDevice("distance sensor1")
distanceSensorLeft = robot.getDevice("distance sensor2")
distanceSensorFront = robot.getDevice("distance sensor3")

distanceSensorRight.enable(timeStep)
distanceSensorLeft.enable(timeStep)
distanceSensorFront.enable(timeStep)

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

# main
def main():
    while robot.step(timeStep) != -1:
        print(numToBlock(distanceSensorLeft.getValue()), numToBlock(distanceSensorFront.getValue()), numToBlock(distanceSensorRight.getValue()))

        speed1 = max_velocity
        speed2 = max_velocity

        # navigazione
        if distanceSensorFront.getValue() < 0.1:
            wheel_left.setVelocity(0)
            wheel_right.setVelocity(0)

            # girare a destra perchè c'è un muro davanti e a sinistra
            if distanceSensorLeft.getValue() < 0.1:
                speed2 = -max_velocity
                speed1 = max_velocity

            # girare a sinistra perchè c'è un muro davanti e a destra
            elif distanceSensorRight.getValue() < 0.1:
                speed2 = max_velocity
                speed1 = -max_velocity

        wheel_left.setVelocity(speed1)
        wheel_right.setVelocity(speed2)

        print("Left motor has spun " + str(leftEncoder.getValue()) + " radians")
        print("Right motor has spun " + str(rightEncoder.getValue()) + " radians")

if __name__ == "__main__":
    main()