from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():
    # Gazebo Sim
    gz_sim = ExecuteProcess(
        cmd=["gz", "sim", "-v4", "-r", "iris_runway.sdf"],
        output="screen",
    )

    # Image bridge
    image_bridge = ExecuteProcess(
        cmd=[
            "ros2",
            "run",
            "ros_gz_bridge",
            "parameter_bridge",
            "/world/iris_runway/model/iris_with_gimbal/model/gimbal/link/pitch_link/"
            "sensor/camera/image"
            "@sensor_msgs/msg/Image"
            "[gz.msgs.Image",
        ],
        output="screen",
    )

    # Camera info bridge
    camera_info_bridge = ExecuteProcess(
        cmd=[
            "ros2",
            "run",
            "ros_gz_bridge",
            "parameter_bridge",
            "/world/iris_runway/model/iris_with_gimbal/model/gimbal/link/pitch_link/"
            "sensor/camera/camera_info"
            "@sensor_msgs/msg/CameraInfo"
            "[gz.msgs.CameraInfo",
        ],
        output="screen",
    )

    # AprilTag detector
    apriltag = Node(
        package="apriltag_ros",
        executable="apriltag_node",
        arguments=[
            "--ros-args",
            "-r",
            "image_rect:=/world/iris_runway/model/iris_with_gimbal/model/gimbal/"
            "link/pitch_link/sensor/camera/image",
            "-r",
            "camera_info:=/world/iris_tag_runway/model/iris_with_gimbal/model/"
            "gimbal/link/pitch_link/sensor/camera/camera_info",
        ],
        # you probably also want a params file here:
        # parameters=[{"tags_36h11.yaml": "..."}]
        output="screen",
    )

    return LaunchDescription(
        [
            gz_sim,
            image_bridge,
            camera_info_bridge,
            apriltag,
        ]
    )
