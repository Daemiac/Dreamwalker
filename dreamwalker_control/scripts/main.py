#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64, String
from std_msgs.msg import Float32
import math
from dreamwalker_control.srv import Service_GUI_Command, Service_GUI_CommandResponse

joint_node = { "shoulder1": "/dreamwalker/shoulder_joint1_position_controller/command", 
				"shoulder2": "/dreamwalker/shoulder_joint2_position_controller/command",
				"shoulder3": "/dreamwalker/shoulder_joint3_position_controller/command",
				"shoulder4": "/dreamwalker/shoulder_joint4_position_controller/command",
				"limb1": "/dreamwalker/limb_joint1_position_controller/command",
				"limb2": "/dreamwalker/limb_joint2_position_controller/command",
				"limb3": "/dreamwalker/limb_joint3_position_controller/command",
				"limb4": "/dreamwalker/limb_joint4_position_controller/command"  }


class Leg():
	""" Construct made of 3 servomotors """
	def __init__(self, name, servo1, servo2, servo3):
		self._name = name
		self._shoulder_joint = Joint(command=servo1, up_limit=30, low_limit=(-30))
		self._limb_joint = Joint(command=servo2, up_limit=90, low_limit=(-90))
		self._knee_joint = Joint(command=servo3, up_limit=150, low_limit=-50)
		self.signal = None
		self.enabled = None

	def reset_leg_position(self, value):
		""" Sets all servomotors to default position """
		self._shoulder_joint._pub.publish(0.0)
		self._limb_joint._pub.publish(0.0)
		self._knee_joint._pub.publish(0.0)
		print "All joints set to 0"


	def is_enabled(self, leg):
		self.signal = leg.data
		if self.signal == self._mark:
			self.enabled = True
			print "Leg enabled: {}".format(self.signal)

		else:
			self.enabled = False
			print "Leg disabled: {}".format(self._mark)


	def move_shoulder_servo(self, value):
		self.value = value.data
		if self.signal == self._mark:
			self._shoulder_joint.set_joint_value(self.value)


	def move_limb_servo(self, value):
		self.value = value.data
		if self.signal == self._mark:
			self._limb_joint.set_joint_value(self.value)


	def move_knee_servo(self, value):
		self.value = value.data
		if self.signal == self._mark:
			self._knee_joint.set_joint_value(self.value)


class Joint():
	def __init__(self, command, up_limit, low_limit):
		self.command = command
		self._pub = rospy.Publisher(self.command, Float64, queue_size=10)
		self.upper_limit = up_limit
		self.lower_limit = low_limit


	def deg2rad(self, angle):
		""" Converts degrees into radians """
		angle = float(angle)
		return angle*(math.pi/180)


	def set_joint_value(self, value):
		""" Publishes recieved value to simulated joint """
		self.value = self.deg2rad(value)
		if self.value >= self.upper_limit:
			self.value = self.upper_limit
		elif self.value <= self.lower_limit:
			self.value = self.lower_limit
		
		self._pub.publish(self.value)
		rospy.loginfo(self.value)


class Robot():
	def __init__(self):
		
		rospy.init_node('Dreamwalker_control')

		rospy.loginfo("Initializing the robot")

		service=rospy.Service('command_service',Service_GUI_Command, self.turn_on_off)
		self.command = 0
	
	def turn_on_off(self, request):
		if request.command=="FORWARD":
			self.command = 1
			return Service_GUI_CommandResponse("Robot going forward")
		elif request.command=="LEFT":
			self.command = 2
			return Service_GUI_CommandResponse("Robot going left")
		elif request.command=="RIGHT":
			self.command = 3
			return Service_GUI_CommandResponse("Robot going right")
		elif request.command=="SPIN_LEFT":
			self.command = 4
			return Service_GUI_CommandResponse("Robot spins left")
		elif request.command=="SPIN_RIGHT":
			self.command = 5
			return Service_GUI_CommandResponse("Robot spins right")
		elif request.command=="BACKWARD":
			self.command = 6
			return Service_GUI_CommandResponse("Robot goes back")
		elif request.command=="STOP":
			self.command = 0
			return Service_GUI_CommandResponse("State: IDLE")

	def run(self):
		rate = rospy.Rate(10)

		while not rospy.is_shutdown():
			if self.command == 0:
				print("Robot is in idle state")
			elif self.command == 1:
				print("Robot goes forward")
			elif self.command == 2:
				print("Robot goes left")
			elif self.command == 3:
				print("Robot goes right")
			elif self.command == 4:
				print("Robot spins left")
			elif self.command == 5:
				print("Robot spins right")
			elif self.command == 6:
				print("Robot goes back")	

			rate.sleep()


if __name__ == '__main__':
	try:
		dreamwalker = Robot()
		dreamwalker.run()

	except rospy.ROSInterruptException:
		pass
