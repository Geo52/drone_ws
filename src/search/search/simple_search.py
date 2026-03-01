import rclpy
from rclpy.node import Node
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL
import time

def main():
    rclpy.init()
    node = Node('simple_takeoff')

    # Create service clients
    arm_client = node.create_client(CommandBool, 'mavros/cmd/arming')
    mode_client = node.create_client(SetMode, 'mavros/set_mode')
    takeoff_client = node.create_client(CommandTOL, 'mavros/cmd/takeoff')

    # Wait for services
    while not arm_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('Waiting for arming service...')
    while not mode_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('Waiting for set_mode service...')
    while not takeoff_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('Waiting for takeoff service...')

    # Set GUIDED mode
    mode_req = SetMode.Request()
    mode_req.custom_mode = 'GUIDED'
    mode_client.call_async(mode_req)
    node.get_logger().info('Set mode to GUIDED')
    time.sleep(1)

    # Arm the drone
    arm_req = CommandBool.Request()
    arm_req.value = True
    arm_client.call_async(arm_req)
    node.get_logger().info('Drone armed')
    time.sleep(1)

    # Takeoff to 10 meters
    takeoff_req = CommandTOL.Request()
    takeoff_req.altitude = 2.0
    takeoff_client.call_async(takeoff_req)
    node.get_logger().info('Taking off to 10 meters')

    rclpy.shutdown()

if __name__ == '__main__':
    main()