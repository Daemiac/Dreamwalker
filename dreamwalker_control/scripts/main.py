#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64, String
import math

joint_node = { "shoulder1": "/dreamwalker/shoulder_joint1_position_controller/command", 
				"shoulder2": "/dreamwalker/shoulder_joint2_position_controller/command",
				"shoulder3": "/dreamwalker/shoulder_joint3_position_controller/command",
				"shoulder4": "/dreamwalker/shoulder_joint4_position_controller/command",
				"limb1": "/dreamwalker/limb_joint1_position_controller/command",
				"limb2": "/dreamwalker/limb_joint2_position_controller/command",
				"limb3": "/dreamwalker/limb_joint3_position_controller/command",
				"limb4": "/dreamwalker/limb_joint4_position_controller/command"  }

class Joint():
	def __init__(self, command):
		self.command = command
		self.pub = rospy.Publisher(self.command, Float64, queue_size=10)

	def idle():
		self.pub.publish(0.0)

	def move(self, x):
		self.pub.publish(x)


def main():
	
	shoulder1 = Joint(joint_node["shoulder1"])
	shoulder2 = Joint(joint_node["shoulder2"])
	shoulder3 = Joint(joint_node["shoulder3"])
	shoulder4 = Joint(joint_node["shoulder4"])
	limb1 = Joint(joint_node["limb1"])
	limb2 = Joint(joint_node["limb2"])
	limb3 = Joint(joint_node["limb3"])
	limb4 = Joint(joint_node["limb4"])

	rospy.init_node('dreamwalker_limb1_position', anonymous=True)
	rate = rospy.Rate(100)

	i = 0
	while not rospy.is_shutdown():
		shoulder1.pub.publish(0.0)
		shoulder2.pub.publish(0.0)
		shoulder3.pub.publish(0.0)
		shoulder4.pub.publish(0.0)
		position = math.sin(i)
		position2 = -math.sin(i)
		limb1.move(position)
		limb2.pub.publish(position)
		limb3.pub.publish(position2)
		limb4.pub.publish(position2)
		rate.sleep()
		i += 0.01

if __name__ == '__main__':
	try:
		main()

	except rospy.ROSInterruptException:
		pass
