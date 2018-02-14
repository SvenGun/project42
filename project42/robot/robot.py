"""Robot module"""

MOTOR_L_FORWARD_PIN = 12
MOTOR_L_BACKWARD_PIN = 16
MOTOR_R_FORWARD_PIN = 20
MOTOR_R_BACKWARD_PIN = 21
MOTOR_GRAB_IN = 19
MOTOR_GRAB_OUT = 26
GRAB_IN_SENSOR = 6
GRAB_OUT_SENSOR = 13
L_IR_SENSOR = 23
R_IR_SENSOR = 24
# Value between 0 and 255 -> dutycycle = 255 / SPEED
MOTOR_SPEED = 64
GRAB_SPEED = 64

class Robot:
    """Represents the robot."""

    def __init__(self, pi):
        self.__pi = pi
        self.is_moving = False

    def __set_pwm(self, pin, val, speed):
        """Sets the GPIO pins using PWM."""

        self.__pi.set_PWM_dutycycle(pin, val * speed)

    def __move(self, l_forward, l_back, r_forward, r_back):
        """Sets the pins to move the robot in a direction."""

        self.__set_pwm(MOTOR_L_FORWARD_PIN, l_forward, MOTOR_SPEED)
        self.__set_pwm(MOTOR_L_BACKWARD_PIN, l_back, MOTOR_SPEED)
        self.__set_pwm(MOTOR_R_FORWARD_PIN, r_forward, MOTOR_SPEED)
        self.__set_pwm(MOTOR_R_BACKWARD_PIN, r_back, MOTOR_SPEED)

    def __move_grab(self, grab_in, grab_out):
        """Sets the pins to move the grab in or out."""

        self.__set_pwm(MOTOR_GRAB_IN, grab_in, GRAB_SPEED)
        self.__set_pwm(MOTOR_GRAB_OUT, grab_out, GRAB_SPEED)

    def follow_line(self):
        """Follows the black line."""

        if self.__pi.read(L_IR_SENSOR) == 1 and self.__pi.read(R_IR_SENSOR) == 1:
            self.hold_position()
            return False
        elif self.__pi.read(L_IR_SENSOR) == 1:
            self.turn_left()
        elif self.__pi.read(R_IR_SENSOR) == 1:
            self.turn_right()
        else:
            self.move_forward()

        return True

    def move_forward(self):
        """Moves the robot forward."""

        self.__move(1, 0, 1, 0)
        self.is_moving = True

    def move_backwards(self):
        """Moves the robot backwards."""

        self.__move(0, 1, 0, 1)
        self.is_moving = True

    def hold_position(self):
        """Stops the movement of the robot."""

        self.__move(0, 0, 0, 0)
        self.is_moving = False

    def turn_left(self):
        """Turns the robot left."""

        self.__move(0, 1, 1, 0)
        self.is_moving = True

    def turn_right(self):
        """Turns the robot right."""

        self.__move(1, 0, 0, 1)
        self.is_moving = True

    def move_grab_in(self):
        """Moves the grab in."""

        while self.__pi.read(GRAB_IN_SENSOR) != 1:
            self.__move_grab(1, 0)

        self.__move_grab(0, 0)

    def move_grab_out(self):
        """Moves the grab out."""

        while self.__pi.read(GRAB_OUT_SENSOR) != 1:
            self.__move_grab(0, 1)

        self.__move_grab(0, 0)
