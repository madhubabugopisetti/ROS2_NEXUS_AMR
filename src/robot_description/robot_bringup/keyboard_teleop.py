import sys, termios, tty, select
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            return sys.stdin.read(1)
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def run(self):
        while rclpy.ok():
            key = get_key()
            if key == '\x03':
                break
            msg = Twist()
            if key == 'w':
                msg.linear.x = 0.5
            elif key == 's':
                msg.linear.x = -0.5
            elif key == 'a':
                msg.angular.z = 0.8
            elif key == 'd':
                msg.angular.z = -0.8
            elif key == 'x':
                pass
            else:
                continue
            self.pub.publish(msg)

def main():
    rclpy.init()
    node = KeyboardTeleop()
    try:
        node.run()
    finally:
        node.pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
