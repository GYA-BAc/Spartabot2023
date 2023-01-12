import wpilib
from ctre import WPI_TalonSRX
from magicbot import MagicRobot
from networktables import NetworkTables, NetworkTablesInstance

from components import DriveTrain

# Download and install stuff on the RoboRIO after imaging
'''py -3 -m robotpy_installer download-python
   py -3 -m robotpy_installer install-python
   py -3 -m robotpy_installer download robotpy
   py -3 -m robotpy_installer install robotpy
   py -3 -m robotpy_installer download robotpy[ctre]
   py -3 -m robotpy_installer install robotpy[ctre]
   py -3 -m robotpy_installer download robotpy[rev]
   py -3 -m robotpy_installer install robotpy[rev]'''

# Push code to RoboRIO (only after imaging)
'''python py/robot/robot.py deploy --skip-tests'''
'''py py/robot/robot.py deploy --skip-tests --no-version-check'''

# if ctre not found
'''py -3 -m pip install -U robotpy[ctre]'''
'''py -3 -m pip install robotpy[ctre]'''

INPUT_SENSITIVITY = .3

class SpartaBot(MagicRobot):

    # MagicRobot automatically makes an instance of DriveTrain
    drivetrain: DriveTrain

    def createObjects(self):
        '''Create motors and stuff here'''

        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd: NetworkTablesInstance = NetworkTables.getTable('SmartDashboard')

        self.drive_controller = wpilib.XboxController(0)

        self.talon_L_1 = WPI_TalonSRX(6)
        self.talon_L_2 = WPI_TalonSRX(9)

        self.talon_R_1 = WPI_TalonSRX(1)
        self.talon_R_2 = WPI_TalonSRX(5)

        # drivetrain
        self.drivetrain = DriveTrain(
            LMotors=[self.talon_L_1, self.talon_L_2],
            RMotors=[self.talon_R_1, self.talon_R_2],
            smart_dashboard=self.sd
        )

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.sd.putValue("Mode", "Teleop")

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        angle = self.drive_controller.getRightX()
        #print(self.drive_controller.getRawAxis(0))
        speed = self.drive_controller.getLeftY()

        #angle, speed = 0.0, 0.0

        if (abs(angle) > INPUT_SENSITIVITY or abs(speed) > INPUT_SENSITIVITY):
            #self.drive.arcadeDrive(-angle * ANGLE_MULTIPLIER, -speed * SPEED_MULTIPLIER, True) NOTE: THIS IS INVERSED?
            self.drivetrain.set_motors(speed, angle)
            self.sd.putValue('Drivetrain: ', 'moving')

        else:
            # reset value to make robot stop moving
            self.drivetrain.set_motors(0.0, 0.0)
            self.sd.putValue('Drivetrain: ', 'static')
        
        self.drivetrain.execute()

        # self.drivetrain's execute() method is automatically called

if __name__ == '__main__':
    wpilib.run(SpartaBot)