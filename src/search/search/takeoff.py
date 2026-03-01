import rclpy
from rclpy.node import Node
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL

class TakeoffNode(Node):
    def __init__(self):
        super().__init__('takeoff_node')

        self.current_state = None

        # Subscriber to drone state
        self.state_sub = self.create_subscription(
            State,
            'mavros/state',
            self.state_cb,
            10
        )

        # Service clients
        self.arming_client = self.create_client(CommandBool, 'mavros/cmd/arming')
        self.mode_client = self.create_client(SetMode, 'mavros/set_mode')
        self.takeoff_client = self.create_client(CommandTOL, 'mavros/cmd/takeoff')

        # Wait for services to be available
        while not self.arming_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for arming service...')
        while not self.mode_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for set_mode service...')
        while not self.takeoff_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for takeoff service...')

        # Start the takeoff process
        self.takeoff()
        

    def state_cb(self, msg):
        self.current_state = msg

    def takeoff(self):
        # Wait until connected
        while rclpy.ok() and (self.current_state is None or not self.current_state.connected):
            self.get_logger().info('Waiting for connection...')
            rclpy.spin_once(self, timeout_sec=0.1)

        # Set GUIDED mode
        req_mode = SetMode.Request()
        req_mode.custom_mode = 'GUIDED'
        self.mode_client.call_async(req_mode)
        self.get_logger().info('Set mode to GUIDED')

        # Arm the drone
        req_arm = CommandBool.Request()
        req_arm.value = True
        self.arming_client.call_async(req_arm)
        self.get_logger().info('Drone armed')

        # Takeoff to 10 meters
        req_takeoff = CommandTOL.Request()
        req_takeoff.altitude = 2.0
        self.takeoff_client.call_async(req_takeoff)
        self.get_logger().info('Taking off to 10 meters')

def main(args=None):
    rclpy.init(args=args)
    node = TakeoffNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()