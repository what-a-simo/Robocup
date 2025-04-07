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
