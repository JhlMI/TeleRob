#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray
import can

class CANBridge(Node):
    def __init__(self):
        super().__init__('can_bridge')
        self.bus = can.interface.Bus(channel='can0', bustype='socketcan')
        self.sub = self.create_subscription(Int16MultiArray, 'cmd_pwm', self.listener_callback, 10)
        self.get_logger().info('Bridge CAN listo')

    def listener_callback(self, msg):
        pwm_left = msg.data[0]
        pwm_right = msg.data[1]
        left_byte  = pwm_left & 0xFF if pwm_left >= 0 else (256 + pwm_left)
        right_byte = pwm_right & 0xFF if pwm_right >= 0 else (256 + pwm_right)
        frame = can.Message(arbitration_id=0x120, data=[left_byte, right_byte], is_extended_id=False)
        try:
            self.bus.send(frame)
            self.get_logger().info(f'CAN → Izq={pwm_left} Der={pwm_right}')
        except can.CanError as e:
            self.get_logger().error(f'Error CAN: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = CANBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
