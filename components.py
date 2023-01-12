from wpilib import MotorControllerGroup

from wpilib.drive import DifferentialDrive
from networktables import NetworkTablesInstance


SPEED_MULTIPLIER = 1
ANGLE_MULTIPLIER = 0.7

def limit(number: float, limits: list) -> float:
    """
    return a number within the limits, returning the limiting number if out of bounds
    number: any number
    limits: list of limits, first element is minimum, second is max
    ex:
        >>> limit(5, [-4, 4])
        >>> 4
    """
    return min(max(number, limits[0]), limits[1])


class DriveTrain:


    def __init__(self, LMotors: list, RMotors: list, smart_dashboard: NetworkTablesInstance):

        # order of talons are subject to change
        # TODO: use phoenix tuner to get order of talon controllers

        self.sd: NetworkTablesInstance = smart_dashboard

        self.left_motors: MotorControllerGroup = MotorControllerGroup(*LMotors)
        self.right_motors: MotorControllerGroup = MotorControllerGroup(*RMotors)

        self.drive: DifferentialDrive = DifferentialDrive(self.left_motors, self.right_motors)

        self.speed: float = 0.0
        self.angle: float = 0.0

    # control method
    def set_motors(self, speed: float, angle: float):
        """
        sets the speed and angle of the motors
        speed: percentage of full speed
        angle: percentage of full rotation, ccw is positive
        Calls the arcadeDrive() method of the DifferentialDrive
        """
        self.speed = limit(speed, [-1, 1])
        self.angle = limit(angle, [-1, 1])

        self.sd.putValue("Speed: ", speed)
        self.sd.putValue("Angle: ", angle)

    # execute is called every iteration of the control loop automatically; no need to manually call
    def execute(self) -> None:
        """reads the data stored by the control methods, and then sends data to output devices such as motors"""
        
        self.drive.arcadeDrive(-self.speed * SPEED_MULTIPLIER, -self.angle * ANGLE_MULTIPLIER, squareInputs=True)
        
        