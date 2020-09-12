#! /usr/bin/env python
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import Range

sonar_node = {"left_sensor": 'sensor/left_sonar',
				"middle_sensor": 'sensor/middle_sonar',
				"right_sensor": 'sensor/right_sonar'}

class Sonar():
	""" Creates a subscriber to read simulated sensor value """
	def __init__(self, topic_name):
		self._name = topic_name
		self._value = rospy.Subscriber(topic_name, Float32, self.reading_value)
		self.reading = 0

	def reading_value(self, msg):
		self.reading = msg.data
		self.reading = round(self.reading, 2)


class SonarSystem():
	def __init__(self):
		rospy.init_node('Sensor_system')

		rospy.loginfo("Setting up the SensorValues node...")

		self._value_pub = rospy.Publisher()

		self.left_sensor = Sonar('sensor1_value')
		self.middle_sensor = Sonar('sensor2_value')
		self.right_sensor = Sonar('sensor3_value')
		self.value_list = [0, 0, 0]
		
	def run(self):
		rate =  rospy.Rate(10)
		while not rospy.is_shutdown():
			self.value_list[0] = self.left_sensor.reading
			self.value_list[1] = self.middle_sensor.reading
			self.value_list[2] = self.right_sensor.reading
			rospy.loginfo("Sensors values: %s", self.value_list)
			rate.sleep()

if __name__ == '__main__':
	
	try:
		sonar_system = SonarSystem()
		sonar_system.run()


	except rospy.ROSInterruptException:
		pass
