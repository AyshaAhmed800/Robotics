# Robotics: Vision Detection for RoboCup

**Author:** Aysha Ahmed  
**Student ID:** 25075964  
**Date:** 25 April 2026  

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
```bash
cd ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run vision_detection robocup_vision
