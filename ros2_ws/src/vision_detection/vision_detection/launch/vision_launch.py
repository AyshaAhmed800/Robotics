#This file made because it ttarts the vision node with one command instead of typing multiple things
from launch import LaunchDescription
from launch_ros.actions import Node
# Launch file has made to start the vision detection node.
# This makes it easier to run the node without typing these long commands in the terminal.
def generate_launch_description():
    return LaunchDescription([
        Node(
            package='vision_detection',
            executable='robocup_vision',
            name='robocup_vision_node',
            output='screen',
# The node subscribes to the /camera/image_raw and publishes ball/goal coordinates.
        )
    ])