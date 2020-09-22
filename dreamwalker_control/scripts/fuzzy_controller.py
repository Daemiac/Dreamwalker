#!/usr/bin/env python
import rospy
import fuzzylab as fl
from std_msgs.msg import Int8
from geometry_msgs.msg import Point


class FuzzyController():
    def __init__(self):

        rospy.init_node('fuzzy_controller')
        rospy.loginfo("Initializing the controller")

        self.min_range = 0.02
        self.max_range = 1
        self.dn = 0.25
        self.dm = 0.5
        self.df = 0.75

        self._obtained_values = rospy.Subscriber('sensor_array', Point, self.update_sensor_values)
        self._steering_value = rospy.Publisher('steering_value', Int8, queue_size=10)
        
        self.sensor_values = [0, 0, 0]
        self.steering_value = -1

    def calculate_fuzzy(self, list):
        fis = fl.sugfis()
        #parametry czujnika
  
        fis.addInput([self.min_range, self.max_range], Name='left_sensor_value')
        fis.addMF('left_sensor_value', 'trapmf', [self.min_range, self.min_range, self.dn, self.dm], Name="CLOSE")
        fis.addMF('left_sensor_value', 'trapmf', [self.dn, self.dm, self.dm, self.df], Name="MEDIUM")
        fis.addMF('left_sensor_value', 'trapmf', [self.dm, self.df, self.max_range, self.max_range], Name="FAR")
        #fl.plotmf(fis, 'input', 0)
        fis.addInput([self.min_range, self.max_range], Name='middle_sensor_value')
        fis.addMF('middle_sensor_value', 'trapmf', [self.min_range, self.min_range, self.dn, self.dm], Name="CLOSE")
        fis.addMF('middle_sensor_value', 'trapmf', [self.dn, self.dm, self.dm, self.df], Name="MEDIUM")
        fis.addMF('middle_sensor_value', 'trapmf', [self.dm, self.df, self.max_range, self.max_range], Name="FAR")
        #fl.plotmf(fis, 'input', 1)
        fis.addInput([self.min_range, self.max_range], Name='right_sensor_value')
        fis.addMF('right_sensor_value', 'trapmf', [self.min_range, self.min_range, self.dn, self.dm], Name="CLOSE")
        fis.addMF('right_sensor_value', 'trapmf', [self.dn, self.dm, self.dm, self.df], Name="MEDIUM")
        fis.addMF('right_sensor_value', 'trapmf', [self.dm, self.df, self.max_range, self.max_range], Name="FAR")
        #fl.plotmf(fis, 'input', 2)

        output_values = [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]

        fis.addOutput([output_values[0], output_values[-1]], Name='COMMAND')
        fis.addMF('COMMAND', 'constant', output_values[0], Name="BACK")
        fis.addMF('COMMAND', 'constant', output_values[2], Name="TURN LEFT")
        fis.addMF('COMMAND', 'constant', output_values[4], Name="FORWARD")
        fis.addMF('COMMAND', 'constant', output_values[6], Name="TURN RIGHT ")
        fis.addMF('COMMAND', 'constant', output_values[8], Name="BACK")

        # rule list
        ruleList = [[0, 0, 0, 0, 1, 1], [0, 0, 1, 3, 1, 1], [0, 0, 2, 3, 1, 1],
                    [0, 1, 0, 0, 1, 1], [0, 1, 1, 0, 1, 1], [0, 1, 2, 3, 1, 1],
                    [0, 2, 0, 2, 1, 1], [0, 2, 1, 2, 1, 1], [0, 2, 2, 2, 1, 1],
                    [1, 0, 0, 1, 1, 1], [1, 0, 1, 1, 1, 1], [1, 0, 2, 3, 1, 1],
                    [1, 1, 0, 1, 1, 1], [1, 1, 1, 2, 1, 1], [1, 1, 2, 3, 1, 1],
                    [1, 2, 0, 2, 1, 1], [1, 2, 1, 2, 1, 1], [1, 2, 2, 2, 1, 1],
                    [2, 0, 0, 1, 1, 1], [2, 0, 1, 1, 1, 1], [2, 0, 2, 1, 1, 1],
                    [2, 1, 0, 1, 1, 1], [2, 1, 1, 1, 1, 1], [2, 1, 2, 2, 1, 1],
                    [2, 2, 0, 2, 1, 1], [2, 2, 1, 2, 1, 1], [2, 2, 2, 2, 1, 1]]

        fis.addRule(ruleList)
        #new_command = fl.evalfis(fis, list)
        #self.interpreter(new_command)
        self.evalfis(list)

    def evalfis(self, list):
        if list[0] <= 0.40 and list[1] >= 0.40 and list[2] >= 0.40:
            self.steering_value = 3
        elif list[0] <= 0.40 and list[1] <= 0.40 and list[2] <= 0.40:
            self.steering_value = 0
        elif list[0] >= 0.40 and list[1] >= 0.40 and list[2] <= 0.40:
            self.steering_value = 2
        else:
            self.steering_value = 1

    def interpreter(self, value):
        if -1.5 > value >= -2:
            print("Fuzzy value: {x} Command: GOING BACK".format(x=value))
        elif -0.5 > value >= -1.5:
            print("Fuzzy value: {x} Command: GOING LEFT".format(x=value))
        elif 0.5 >= value >= -0.5:
            print("Fuzzy value: {x} Command: GOING FORWARD".format(x=value))
        elif 1.5 >= value > 0.5:
            print("Fuzzy value: {x} Command: GOING RIGHT".format(x=value))
        elif 2 >= value > 1.5:
            print("HONK HONK BACKWARD")
        else:
            print("Cos jest nie tak")

    def update_sensor_values(self, data):
        self.sensor_values[0] = data.x
        self.sensor_values[1] = data.y
        self.sensor_values[2] = data.z

    def run(self):
        rate =  rospy.Rate(5)
        while not rospy.is_shutdown():
            rospy.loginfo("Sensors values: %s", self.sensor_values)            
            self.calculate_fuzzy(self.sensor_values)
            rospy.loginfo(self.steering_value)
            self._steering_value.publish(data=self.steering_value)
            rate.sleep()


def interpreter(value):
    if -1.5 > value >= -2:
        print("Fuzzy value: {x} Command: GOING BACK".format(x=value))
    elif -0.5 > value >= -1.5:
        print("Fuzzy value: {x} Command: GOING LEFT".format(x=value))
    elif 0.5 >= value >= -0.5:
        print("Fuzzy value: {x} Command: GOING FORWARD".format(x=value))
    elif 1.5 >= value > 0.5:
        print("Fuzzy value: {x} Command: GOING RIGHT".format(x=value))
    elif 2 >= value > 1.5:
        print("HONK HONK BACKWARD")
    else:
        print("Cos jest nie tak")



if __name__ == '__main__':
    try:
        controller = FuzzyController()
        controller.run()


    except rospy.ROSInterruptException:
        pass
