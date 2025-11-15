#!/usr/bin/env python3
import can, time, struct

bus = can.interface.Bus(channel='can0', bustype='socketcan')

def send_pwm(left, right):
    left  = max(-100, min(100, left))
    right = max(-100, min(100, right))
    l_byte = left & 0xFF if left >= 0 else (256 + left)
    r_byte = right & 0xFF if right >= 0 else (256 + right)
    msg = can.Message(arbitration_id=0x120, data=[l_byte, r_byte], is_extended_id=False)
    try:
        bus.send(msg)
    except can.CanError as e:
        print(" Error enviando CAN:", e)

def read_feedback():
    msg = bus.recv(timeout=0.05)
    if msg and msg.arbitration_id == 0x130 and msg.dlc >= 4:
        rpm_left  = struct.unpack('>h', bytes(msg.data[0:2]))[0] / 10.0
        rpm_right = struct.unpack('>h', bytes(msg.data[2:4]))[0] / 10.0
        print(f" RPM Izq={rpm_left:6.2f} | Der={rpm_right:6.2f}")
        return rpm_left, rpm_right
    return None, None

if __name__ == "__main__":
    print(" CAN maestro: enviando PWM y recibiendo RPM...")
    pwm_l, pwm_r, step = -50, 50, 10
    last_send = time.time()
    while True:
        now = time.time()
        if now - last_send >= 1.0:
            send_pwm(pwm_l, pwm_r)
            pwm_l += step
            pwm_r -= step
            if abs(pwm_l) > 100:
                step *= -1
            last_send = now
        read_feedback()
