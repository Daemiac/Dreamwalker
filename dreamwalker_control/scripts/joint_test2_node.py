#!/user/bin/env python

print "huehuehuehue"

class Leg():
	""" Construct made of 3 servomotors """
	def __init__(self, mark, servo1, servo2, servo3):
		self._mark = mark
		self._shoulder_joint = Joint(command=servo1, up_limit=30, low_limit=(-30))
		self._limb_joint = Joint(command=servo2, up_limit=90, low_limit=(-90))
		self._knee_joint = Joint(command=servo3, up_limit=150, low_limit=0)
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


	def swing_joint(self):
			pass



class Joint():
	""" Represents servomotor """
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




def main():
	
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




if __name__ == '__main__':
	
	rospy.init_node('joint_test1')
	r = rospy.Rate(100)

	try:
		main()

	except rospy.ROSInterruptException:
		pass
