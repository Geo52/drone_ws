from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
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
    apriltag_ros = Node(
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
    mavros = TimerAction(
        period=5.0,  # wait 5s for SITL to be ready
        actions=[
            ExecuteProcess(
                cmd=[
                    "ros2", "launch", "mavros", "apm.launch",
                    "fcu_url:=udp://:14550@127.0.0.1:14555",
                    "gcs_url:=udp://@",
                ],
                output="screen",
            )
        ],
    )
    

    search = Node(
        package="search",
        executable="search",
    )

    return LaunchDescription(
        [
            gz_sim,
            image_bridge,
            camera_info_bridge,
            apriltag_ros,
            mavros,
            # search
        ]
    )
