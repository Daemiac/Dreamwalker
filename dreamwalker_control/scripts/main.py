#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64, String
from std_msgs.msg import Float32
import math
from dreamwalker_control.srv import Service_GUI_Command, Service_GUI_CommandResponse
import numpy

joint_node = { "shoulder1": "/dreamwalker/shoulder_joint1_position_controller/command", 
				"shoulder2": "/dreamwalker/shoulder_joint2_position_controller/command",
				"shoulder3": "/dreamwalker/shoulder_joint3_position_controller/command",
				"shoulder4": "/dreamwalker/shoulder_joint4_position_controller/command",
				"limb1": "/dreamwalker/limb_joint1_position_controller/command",
				"limb2": "/dreamwalker/limb_joint2_position_controller/command",
				"limb3": "/dreamwalker/limb_joint3_position_controller/command",
				"limb4": "/dreamwalker/limb_joint4_position_controller/command",
				"knee1": "/dreamwalker/knee_joint1_position_controller/command",
				"knee2": "/dreamwalker/knee_joint2_position_controller/command",
				"knee3": "/dreamwalker/knee_joint3_position_controller/command",
				"knee4": "/dreamwalker/knee_joint4_position_controller/command" }



class Leg():
	""" Construct made of 3 servomotors """
	def __init__(self, name, servo1, servo2, servo3):
		self._name = name
		self._shoulder_joint = Joint(command=servo1, up_limit=30, low_limit=(-30))
		self._limb_joint = Joint(command=servo2, up_limit=90, low_limit=(-90))
		self._knee_joint = Joint(command=servo3, up_limit=150, low_limit=-50)
		
		# zmienne na potrzeby skakania jak kretyn
		self.base_position = [0.0, numpy.radians(-45), numpy.radians(75)]
		self.enabled = None
		self.jump_point = [0.0, 0.0, 0.0]

		# przechowuje informacje na temat aktualnej pozycji nogi
		self.current_leg_pos = [0, -45, 75]

		self.test_leg_pos = [0, -75, 110]


	def set_idle_position(self):
		""" Sets all servomotors to default position """
		self._shoulder_joint._pub.publish(self.base_position[0])
		self._limb_joint._pub.publish(self.base_position[1])
		self._knee_joint._pub.publish(self.base_position[2])

	def move_to_pos(self, position):
		angle = position


	def move_to_point(self):
		""" Moves the leg to defined point """
		shoulder_angle = self.test_leg_pos[0]
		limb_angle = self.test_leg_pos[1]
		knee_angle = self.test_leg_pos[2]

		while(self.current_leg_pos[0]!=shoulder_angle and self.current_leg_pos[1]!=limb_angle and self.current_leg_pos!=knee_angle):
			# shoulder joint
			if shoulder_angle > self.current_leg_pos[0]:
				self.current_leg_pos[0] = self.current_leg_pos[0]+1
				self._shoulder_joint._pub.publish(numpy.radians(self.current_leg_pos[0]))
				print(self.current_leg_pos[0])
			elif shoulder_angle < self.current_leg_pos[0]:
				self.current_leg_pos[0] = self.current_leg_pos[0]-1
				self._shoulder_joint._pub.publish(numpy.radians(self.current_leg_pos[0]))
				print(self.current_leg_pos[0])

			#limb joint
			if limb_angle > self.current_leg_pos[1]:
				self.current_leg_pos[1] = self.current_leg_pos[1]+1
				self._limb_joint._pub.publish(numpy.radians(self.current_leg_pos[1]))
			elif limb_angle < self.current_leg_pos[1]:
				self.current_leg_pos[1] = self.current_leg_pos[1]-1
				self._limb_joint._pub.publish(numpy.radians(self.current_leg_pos[1]))

			# knee joint
			if knee_angle > self.current_leg_pos[2]:
				self.current_leg_pos[2] = self.current_leg_pos[2]+1
				self._knee_joint._pub.publish(numpy.radians(self.current_leg_pos[2]))
			elif shoulder_angle < self.current_leg_pos[2]:
				self.current_leg_pos[2] = self.current_leg_pos[2]-1
				self._knee_joint._pub.publish(numpy.radians(self.current_leg_pos[2]))
			rospy.sleep(0.1)

		print("Leg moved!")


	def prowl_move(self):
		self._shoulder_joint._pub.publish(0.0)
		self._limb_joint._pub.publish(numpy.radians(-75))
		self._knee_joint._pub.publish(numpy.radians(110))


	def jump_move(self):
		self._shoulder_joint._pub.publish(self.jump_point[0])
		self._limb_joint._pub.publish(self.jump_point[1])
		self._knee_joint._pub.publish(self.jump_point[2])



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
		# leg objects
		self._leg1 = Leg(name="FL", servo1=joint_node["shoulder1"], servo2=joint_node["limb1"], servo3=joint_node["knee1"])
		self._leg2 = Leg(name="FR", servo1=joint_node["shoulder2"], servo2=joint_node["limb2"], servo3=joint_node["knee2"])
		self._leg3 = Leg(name="BL", servo1=joint_node["shoulder3"], servo2=joint_node["limb3"], servo3=joint_node["knee3"])
		self._leg4 = Leg(name="BR", servo1=joint_node["shoulder4"], servo2=joint_node["limb4"], servo3=joint_node["knee4"])

	def set_idle(self):
		self._leg1.set_idle_position()
		self._leg2.set_idle_position()
		self._leg3.set_idle_position()
		self._leg4.set_idle_position()

	def set_jump(self):
		self._leg1.jump_move()
		self._leg2.jump_move()
		self._leg3.jump_move()
		self._leg4.jump_move()

	def prowl(self):
		self._leg1.prowl_move()
		self._leg2.prowl_move()
		self._leg3.prowl_move()
		self._leg4.prowl_move()
	
	def turn_on_off(self, request):
		if request.command=="FORWARD":
			self.command = 1
			print("Robot jumps")
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
			print("Robot goes to idle state")
			return Service_GUI_CommandResponse("State: IDLE")

	def run(self):
		rate = rospy.Rate(20)

		while not rospy.is_shutdown():
			if self.command == 0:
				try:
					self.set_idle()
				except TypeError:
					print("something is no yes")
			elif self.command == 1:
				try:
					self.prowl()
					rospy.sleep(0.5)
					self.set_idle()
					rospy.sleep(0.5)
					self.set_jump()
					rospy.sleep(0.5)
					self.set_idle()
					rospy.sleep(0.5)
				except TypeError:
					print("something is even worse")
			elif self.command == 2:
				self._leg1.move_to_point()
			elif self.command == 3:
				print("Robot goes right")
			elif self.command == 4:
				print("Robot spins left")
			elif self.command == 5:
				print("Robot spins right")
			elif self.command == 6:
				try:
					self.prowl()
				except TypeError:
					print("Welcome to Uganda")	

			rate.sleep()


if __name__ == '__main__':
	try:
		dreamwalker = Robot()
		dreamwalker.run()

	except rospy.ROSInterruptException:
		pass
