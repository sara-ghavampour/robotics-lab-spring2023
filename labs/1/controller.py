#!/usr/bin/env python3
import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import String,Int32
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class TurtleController(Node):
    
    def __init__(self):
        super().__init__("controller")
        self.chaser_x_ = 0
        self.chaser_y_ = 0
        self.chaser_angle_ = 0
        self.spawned_x_ = 0
        self.spawned_y_ = 0
        self.target_spawn = 0
        self.get_knowledge()
        self.chasing_allowed = False
        # self.spawned_position_subscriber_ = self.create_subscription(Pose, "spawned/pose", self.set_spawned_position, 10)        
        # self.chaser_position_subscriber_ = self.create_subscription(Pose, "turtle1/pose", self.set_chaser_position, 10)        
        # self.velocity_publisher_ = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.subscription = self.create_subscription(Int32,'killtopic',self.listener_kill_callback,10)
        self.subscription

    def set_spawned_position(self, position):
        self.spawned_x_ = position.x
        self.spawned_y_ = position.y
        
    def set_chaser_position(self, position):
        self.chaser_x_ = position.x
        self.chaser_y_ = position.y
        self.chaser_angle_ = position.theta
        
        self.chaser_to_turtle() 
        

    def chaser_to_turtle(self):
        velocity = Twist()
        P_LINEAR = 2.0
        P_ANGULAR = 6.0
        
        distance = math.sqrt(((self.spawned_x_-self.chaser_x_)**2) + ((self.spawned_y_-self.chaser_y_)**2))
        desired_angle = math.atan2(self.spawned_y_-self.chaser_y_, self.spawned_x_-self.chaser_x_)
        
        diff = desired_angle-self.chaser_angle_
        if diff > math.pi:
            diff -= 2*math.pi
        elif diff < -1*math.pi:
            diff += 2*math.pi
            
        velocity.angular.z = P_ANGULAR * (diff)
        velocity.linear.x = P_LINEAR * distance
        
        self.velocity_publisher_.publish(velocity)

    def listener_kill_callback(self,kill_result):
        if kill_result.data==10 and not self.chasing_allowed: # go for chasing, yay!
            self.get_logger().info('I heard: "%s"' % kill_result.data)
            self.chasing_allowed = True
            self.target_spawn+=1
            self.get_knowledge() # get data to find next victom
            self.chasing_allowed = False # next


    def get_knowledge(self):
        self.get_logger().info('in get_knowledge ----------------------' )
        self.spawned_position_subscriber_ = self.create_subscription(Pose, "spawned_"+str(self.target_spawn)+"/pose", self.set_spawned_position, 10)        
        self.chaser_position_subscriber_ = self.create_subscription(Pose, "turtle1/pose", self.set_chaser_position, 10)        
        self.velocity_publisher_ = self.create_publisher(Twist, "turtle1/cmd_vel", 10)

        


def main(args=None):
    rclpy.init(args=args)
    controller = TurtleController()
    rclpy.spin(controller)
    rclpy.shutdown()

if __name__ == '__main__':
    main()




