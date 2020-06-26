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

	def SetJointValue(self, value):
		shoulder_value = value.data
	
		shoulder_joint = Joint(joint_node["shoulder1"])
		shoulder_joint.pub.publish(float(shoulder_value))
		rospy.loginfo(shoulder_value)


def PublishPositions(leg):
	chosen_Leg = leg.data

	if chosen_Leg == "FL":
		rospy.loginfo("FrontLeft leg chosen!")
	elif chosen_Leg == "FR":
		rospy.loginfo("FrontRight leg chosen!")
	elif chosen_Leg == "BL":
		rospy.loginfo("backLeft leg chosen!")
	elif chosen_Leg == "BR":
		rospy.loginfo("BackRight leg chosen!")



def main():
	rospy.loginfo("Test_node initialized, let's get started!")
	chosen_leg_sub = rospy.Subscriber("chosenLeg", String, PublishPositions)

	shoulder_joint = Joint(joint_node["shoulder1"])

	shoulder_value_sub = rospy.Subscriber("shoulder_value", String, shoulder_joint.SetJointValue)
	rospy.spin()
	
		

if __name__ == '__main__':
	
	rospy.init_node('joint_test1')
	r = rospy.Rate(100)

	try:
		main()

	except rospy.ROSInterruptException:
		pass
