#!/usr/bin/env python3
import can, struct, time

bus = can.interface.Bus(channel='can0', bustype='socketcan')

def send_setpoints(rpm_left, rpm_right):
    # escala x10 para mantener resolución décima
    sp_left  = int(rpm_left * 10)
    sp_right = int(rpm_right * 10)
    data = struct.pack('>hh', sp_left, sp_right)
    msg = can.Message(arbitration_id=0x120, data=list(data), is_extended_id=False)
    bus.send(msg)

def read_feedback():
    msg = bus.recv(timeout=0.05)
    if msg and msg.arbitration_id == 0x130:
        rpm_left, rpm_right = struct.unpack('>hh', bytes(msg.data[0:4]))
        print(f" RPM Izq={rpm_left/10:.1f} | Der={rpm_right/10:.1f}")

if __name__ == "__main__":
    print("Enviando setpoints RPM y leyendo feedback...")
    setpoints = [(-80, 0)]
    while True:
        for sp in setpoints:
            send_setpoints(*sp)
            t0 = time.time()
            while time.time() - t0 < 2:
                read_feedback()
