# Robotics: Vision Detection for RoboCup

**Author:** Aysha Ahmed  
**Student ID:** 25075964  
**Date:** 26 April 2026  

## Project Description:
This project I have made implements a vision detection system for a RoboCup humanoid robot. The robot detects:
- **Ball** (green bounding circle with a written "BALL" text).
- **Goalpost** (blue bounding rectangle with a written "GOALPOST" text).
- **Field lines** (two yellow lines overlay).

The image shows:
- Green circle around the ball labelled "BALL".
- Blue rectangle around the goalpost labelled "GOALPOST".
- Yellow lines representing the detected field lines.

## How It Works:
1. Camera subscribes to `/camera/image_raw`
2. Image being converted to HSV color space.
3. Color masking which isolates the ball, goalpost, and lines.
4. Contour detection finds the objects.
5. Coordinates published to `/ball_coords` and `/goal_coords`.

## Files:
- `vision_node.py` - Main detection code.
- `launch/vision_launch.py` - Launch file.
- `detection_sample.jpg` - Sample output image.

## Technologies Used:
- ROS2 Jazzy
- Python 3
- OpenCV
- GitHub Codespaces

## How to Run

### Terminal 1: Run the Vision Node

```bash
cd /workspaces/Robotics/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
/workspaces/Robotics/ros2_ws/install/vision_detection/bin/robocup_vision
```

###Terminal 2: Run the Test Publisher

```bash
cd /workspaces/Robotics/ros2_ws
source /opt/ros/jazzy/setup.bash
python3 -c "
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class TestPub(Node):
    def __init__(self):
        super().__init__('test_pub')
        self.pub = self.create_publisher(Image, '/camera/image_raw', 10)
        self.bridge = CvBridge()
        self.timer = self.create_timer(2.0, self.pub_img)
        self.get_logger().info('Publishing test images')
        
    def pub_img(self):
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.circle(img, (320, 240), 50, (0, 255, 0), -1)
        cv2.rectangle(img, (500, 150), (600, 400), (255, 0, 0), 3)
        cv2.line(img, (0, 350), (640, 350), (0, 255, 255), 5)
        cv2.line(img, (0, 400), (640, 400), (0, 255, 255), 5)
        msg = self.bridge.cv2_to_imgmsg(img, 'bgr8')
        self.pub.publish(msg)
        self.get_logger().info('Published test image')

rclpy.init()
node = TestPub()
rclpy.spin(node)
"
