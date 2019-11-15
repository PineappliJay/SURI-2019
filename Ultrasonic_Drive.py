from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from picar import front_wheels
from picar import back_wheels
import picar
import sys

picar.setup()

ua_left = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
ua_right = Ultrasonic_Avoidance.Ultrasonic_Avoidance(16)
ua_front = Ultrasonic_Avoidance.Ultrasonic_Avoidance(12)

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

forward_speed = 0
correction = 0
ls = []
rs = []

def stop():
    bw.stop()
    fw.turn_straight()

def reading_sides():

    print('...measuring left...')
    for x in range(0,10):
        left_storage = ua_left.get_distance()
        ls.append(left_storage)
    
    print('...measuring right...')
    for x in range(0,10):
        right_storage = ua_right.get_distance()
        rs.append(right_storage)
    
    return ls
    return rs

def average(ls, rs):
    return sum(ls)/len(ls)
    return sum(rs)/len(rs)

def calibration():

    reading_sides()

    left_sum = average(ls)
    right_sum = average(rs)

    print('left average : ', left_sum)
    print('right average : ', right_sum)

    if 1 <= left_sum <= right_sum:
        l = 1
        print('left tracking is on')
    else:
        l = 0
        print('left tracking is off')
    
    if 1 <= right_sum <= left_sum:
        r = 1
        print('right tracking is on')
    else:
        r = 0
        print('right tracking is off')

def drive():

    calibration()

    while True:
        avoid()
        if l ==1:
            left_distance = ua_left.get_distance()
            if left_sum < left_distance:
                print('move left')
                angle = 90 - (left_distance - left_sum)
                if angle > correction:
                    angle = 90 - correction
                bw.forward()
                fw.turn(angle)
                bw.speed = forward_speed
            elif left_sum > left_distance:
                print('move right')
                angle = 90 + (left_sum - left_distance)
                if angle > correction:
                    angle = 90 + correction
                bw.forward()
                fw.turn(angle)
                bw.speed = forward_speed
        if r == 1:
            right_distance = ua_right.get_distance()
            bw.speed = forward_speed
            if right_sum < right_distance:
                print('move left')
                angle = 90 + (right_distance - right_sum)
                if angle > correction:
                    angle = 90 + correction
                fw.turn(angle)
                bw.forward()
                bw.speed = forward_speed
            elif left_sum > left_distance:
                print('move right')
                angle = 90 + (left_sum - left_distance)
                if angle > correction:
                    angle = 90 + correction
                bw.forward()
                fw.turn(angle)
                bw.speed = forward_speed

if __name__ == "__main__":
    try:
        drive()
    except KeyboardInterrupt:
        sys.exit()
