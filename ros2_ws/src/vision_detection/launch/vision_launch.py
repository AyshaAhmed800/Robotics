from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='vision_detection',
            executable='robocup_vision',
            name='robocup_vision_node',
            output='screen',
        )
    ])
