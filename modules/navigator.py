from math import acos, radians, sin

ROBOT_DIMENSION = 0.01
DEFAULT_SPEED = 0.005
TRUCK_LENGHT = 0.05
TURN_CONSTANT = 1

Kp = 0.002
Ki = 0.00005
Kd = 0.0005


def get_angle_diff(angle1, angle2):
    return (angle1 - angle2 + 180) % 360 - 180


def get_turn_period(angle1, angle2):
    return 2/TURN_CONSTANT*acos(1-(TURN_CONSTANT*TRUCK_LENGHT)/(2*DEFAULT_SPEED)*abs(radians(get_angle_diff(angle1, angle2))))


def get_truck_angle(timer, turn_period):
    if timer/1000 <= turn_period/2:
        return TURN_CONSTANT*timer
    return TURN_CONSTANT*(turn_period-timer)


class Navigator:

    def __init__(self):
        self.sum_error = 0
        self.diff_error = 0
        self.prev_error = 0
        self.start_turn_time = 0
        self.end_turn_time = 0

    def get_motor_speed(self, real_position, current_planned_position, next_planned_position, timer):
        if not next_planned_position:
            self.clear()
            return (0, 0)
        if current_planned_position[2] != next_planned_position[2] or timer/1000 < self.end_turn_time:
            self.sum_error = 0
            self.diff_error = 0
            self.prev_error = 0
            turn_period = get_turn_period(
                radians(current_planned_position[2]), radians(next_planned_position[2]))
            if not self.start_turn_time:
                self.start_turn_time = timer/1000
                self.end_turn_time = self.start_turn_time + turn_period
            if timer/1000-self.start_turn_time <= turn_period/2:
                omega = DEFAULT_SPEED/TRUCK_LENGHT * \
                    sin(get_truck_angle(timer/1000 - self.start_turn_time,
                                        turn_period)) + TURN_CONSTANT
            else:
                omega = DEFAULT_SPEED/TRUCK_LENGHT * \
                    sin(get_truck_angle(timer/1000 - self.start_turn_time,
                                        turn_period)) - TURN_CONSTANT
        else:
            self.start_turn_time = 0
            self.end_turn_time = 0
            error = radians(get_angle_diff(
                real_position[2], current_planned_position[2]))
            self.sum_error += error
            self.diff_error = error - self.prev_error
            self.prev_error = error
            omega = error * Kp + self.sum_error * Ki + self.diff_error * Kd
        return (DEFAULT_SPEED + omega*ROBOT_DIMENSION/2, DEFAULT_SPEED - omega*ROBOT_DIMENSION/2)

    def clear(self):
        print('Navigator : Clearing data...')
        self.sum_error = 0
        self.diff_error = 0
        self.prev_error = 0
        self.start_turn_time = 0
