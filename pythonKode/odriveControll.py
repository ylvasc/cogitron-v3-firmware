import odrive
from odrive.enums import *
import time

oDrive1 = odrive.find_any()


def configure_motors():
    oDrive1.config.enable_brake_resistor
    oDrive1.config.brake_resistance = 0.55
    oDrive1.config.dc_max_negative_current = -0.01

    # motor1
    oDrive1.axis1.motor.config.current_lim = 10
    oDrive1.axis1.controller.config.vel_limit = 2
    oDrive1.axis1.motor.config.torque_constant = 8.27 / 270
    oDrive1.axis1.motor.config.pole_pairs = 7
    oDrive1.axis1.motor.config.motor_type = 0
    oDrive1.axis1.controller.config.vel_limit = 4
    oDrive1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    while oDrive1.axis1.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)

    # motor2
    # oDrive1.axis0.motor.config.current_lim = 10
    # oDrive1.axis0.controller.config.vel_limit = 2
    # oDrive1.axis0.motor.config.torque_constant = 8.27/270
    # oDrive1.axis0.motor.config.pole_pairs = 7
    # oDrive1.axis0.motor.config.motor_type = 0
    # oDrive1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    # while oDrive1.axis0.current_state != AXIS_STATE_IDLE:
    #     time.sleep(0.1)



def trajectory_controll():
    oDrive1.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    oDrive1.axis1.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ

    oDrive1.axis1.trap_traj.config.vel_limit = 3
    oDrive1.axis1.trap_traj.config.accel_limit = 1
    oDrive1.axis1.trap_traj.config.decel_limit = 1
    oDrive1.axis1.controller.config.inertia = 0

def filtered_controll():
    oDrive1.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    oDrive1.axis1.controller.config.input_filter_bandwidth = 2.0
    oDrive1.axis1.controller.config.input_mode = INPUT_MODE_POS_FILTER

def move_absolute():
    run = True
    while run == True:
        print(oDrive1.axis1.controller.input_pos)
        x = input("set input")
        if x == 'e':
         break
        else:
            oDrive1.axis1.controller.input_pos = float(x)

def move_relative():
    run = True
    while run == True:
        print(oDrive1.axis1.controller.input_pos)
        x = input("set input")
        if x == 'e':
            break
        else:
            oDrive1.axis1.controller.move_incremental(x, False)
            #To set the goal relative to the current actual position, use 'from_goal_point = False'
            #To set the goal relative to the previous destination, use 'from_goal_point = True'

#funksjon for å bevege arm til sted i kordinatsystem
def inverse_kinematics():
    print("inverse kinematics")

def main():
    #konfigurer motorene
    configure_motors()

    #velg inputmode
    inputMode = input("select inputmode 1, 2 (trajectory), 3 (filtered)")
    if inputMode == '1':
        oDrive1.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    elif inputMode == '2':
        trajectory_controll()
    elif inputMode == '3':
        filtered_controll()

    #posisjons kontroll relativ til forige posisjon eller bare bassert på absolutt posisjon
    positionMode = input('select position mode 1 (kinematics), 2 (move relative), 3 (move absolute')
    if positionMode == '1':
        inverse_kinematics()
    elif positionMode == '2':
        move_relative()
    elif positionMode == '3':
        move_absolute()




main()

