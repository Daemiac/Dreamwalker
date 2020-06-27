#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64, String
import math


class Leg():
	def __init__(self, servo1, servo2, servo3):
		self.shoulder_joint = Joint(command=servo1, up_limit=(math.pi/12), low_limit=(math.pi/-12))
		self.limb_joint = Joint(command=servo2, up_limit=(math.pi/2), low_limit=(math.pi/-2))
		self.knee_joint = Joint(command=servo3, up_limit=(2*math.pi/3), low_limit=0)


	def reset_leg_position(self, value):
		self.shoulder_joint.pub.publish(0.0)
		self.limb_joint.pub.publish(0.0)
		self.knee_joint.pub.publish(0.0)



class Joint():
	def __init__(self, command, up_limit, low_limit):
		self.command = command
		self.pub = rospy.Publisher(self.command, Float64, queue_size=10)
		self.upper_limit = up_limit
		self.lower_limit = low_limit


	def set_joint_value(self, value):
		self.value = value.data

		if self.value >= self.upper_limit:
			self.value = self.upper_limit
		elif self.value <= self.lower_limit:
			self.value = self.lower_limit
		
		self.pub.publish(self.value)
		rospy.loginfo(self.value)


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

	joint_node = { "shoulder1": "/dreamwalker/shoulder_joint1_position_controller/command", 
				"shoulder2": "/dreamwalker/shoulder_joint2_position_controller/command",
				"shoulder3": "/dreamwalker/shoulder_joint3_position_controller/command",
				"shoulder4": "/dreamwalker/shoulder_joint4_position_controller/command",
				"limb1": "/dreamwalker/limb_joint1_position_controller/command",
				"limb2": "/dreamwalker/limb_joint2_position_controller/command",
				"limb3": "/dreamwalker/limb_joint3_position_controller/command",
				"limb4": "/dreamwalker/limb_joint4_position_controller/command",
				"knee1": "/dreamwalker/knee_joint1_position_controller/command" }

	rospy.loginfo("Test_node initialized, let's get it started!")
	chosen_leg_sub = rospy.Subscriber("chosenLeg", String, PublishPositions)

	leg1 = Leg(servo1=joint_node["shoulder1"], servo2=joint_node["limb1"], servo3=joint_node["knee1"])

	shoulder_value_sub = rospy.Subscriber("shoulder_value", Float64, leg1.shoulder_joint.set_joint_value)
	arm_value_sub = rospy.Subscriber("limb_value", Float64, leg1.limb_joint.set_joint_value)
	knee_value_sub = rospy.Subscriber("knee_value", Float64, leg1.knee_joint.set_joint_value)
	
	reset_pos = rospy.Subscriber("reset_position", String, leg1.reset_leg_position)

	rospy.spin()
	
		

if __name__ == '__main__':
	
	rospy.init_node('joint_test1')
	r = rospy.Rate(100)

	try:
		main()

	except rospy.ROSInterruptException:
		pass
