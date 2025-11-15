import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/j1nzo/Telerob/Ros2_test/Telerob_ws/install/can_bridge'
