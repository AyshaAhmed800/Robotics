#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
RoboCup Vision Detection System
Author: Aysha Ahmed
Date: April 2026
Detects: Ball, Goalpost, Field Lines
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge
import cv2
import numpy as np

class RoboCupVision(Node):
    def __init__(self):
        super().__init__('aysha_robocup_vision')
        self.get_logger().info('Aysha RoboCup Vision System Started')
        
        # Image converter
        self.img_converter = CvBridge()
        
        # Publishers (renamed)
        self.ball_pub = self.create_publisher(Float32MultiArray, '/ball_coords', 10)
        self.goal_pub = self.create_publisher(Float32MultiArray, '/goal_coords', 10)
        
        # Subscriber
        self.cam_sub = self.create_subscription(Image, '/camera/image_raw', self.process_frame, 10)
        
        # Ball color range (orange)
        self.ball_low = np.array([0, 100, 100])
        self.ball_high = np.array([10, 255, 255])
        
        # Goalpost color range (red)
        self.goal_low = np.array([170, 100, 100])
        self.goal_high = np.array([180, 255, 255])

    def process_frame(self, msg):
        try:
            current_frame = self.img_converter.imgmsg_to_cv2(msg, 'bgr8')
        except:
            return
        
        analysed_frame = self.analyze_image(current_frame)
        cv2.imshow('Aysha Robot Vision', analysed_frame)
        cv2.waitKey(1)

    def analyze_image(self, frame):
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Find ball
        ball_xy = self.locate_ball(hsv_img, frame)
        if ball_xy:
            self.send_coords(self.ball_pub, ball_xy)
        
        # Find goalpost
        goal_xy = self.locate_goal(hsv_img, frame)
        if goal_xy:
            self.send_coords(self.goal_pub, goal_xy)
        
        # Find lines
        self.find_field_lines(frame)
        
        return frame

    def locate_ball(self, hsv_img, frame):
        ball_mask = cv2.inRange(hsv_img, self.ball_low, self.ball_high)
        shapes, _ = cv2.findContours(ball_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if shapes:
            biggest_shape = max(shapes, key=cv2.contourArea)
            area = cv2.contourArea(biggest_shape)
            
            if area > 200:
                M = cv2.moments(biggest_shape)
                if M['m00'] != 0:
                    center_x = int(M['m10'] / M['m00'])
                    center_y = int(M['m01'] / M['m00'])
                    
                    cv2.circle(frame, (center_x, center_y), 20, (0, 255, 0), 3)
                    cv2.putText(frame, 'BALL', (center_x-30, center_y-30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    self.get_logger().info(f'Ball found at ({center_x}, {center_y})')
                    return (center_x, center_y)
        return None

    def locate_goal(self, hsv_img, frame):
        goal_mask = cv2.inRange(hsv_img, self.goal_low, self.goal_high)
        goal_shapes, _ = cv2.findContours(goal_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for shape in goal_shapes:
            area = cv2.contourArea(shape)
            if area > 500:
                x, y, w, h = cv2.boundingRect(shape)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
                cv2.putText(frame, 'GOALPOST', (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                self.get_logger().info(f'Goal found at ({x+w//2}, {y+h//2})')
                return (x + w//2, y + h//2)
        return None

    def find_field_lines(self, frame):
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_img, 50, 150)
        line_segments = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        
        if line_segments is not None:
            for segment in line_segments:
                x1, y1, x2, y2 = segment[0]
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 3)

    def send_coords(self, publisher, position):
        msg = Float32MultiArray()
        msg.data = [float(position[0]), float(position[1])]
        publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RoboCupVision()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('System stopped by Aysha')
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()