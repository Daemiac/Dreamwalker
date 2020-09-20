#!/usr/bin/env python

import fuzzylab as fl
import random


def generate_fake_reading():
    min_range = 0.02
    max_range = 2
    x = round(random.uniform(min_range, max_range), 2)
    y = round(random.uniform(min_range, max_range), 2)
    z = round(random.uniform(min_range, max_range), 2)
    reading = [x, y, z]
    return reading


def fuzzy_controller(list):
    fis = fl.sugfis()
    #parametry czujnika
    min_range = 0.02
    max_range = 2

    dn = 0.5
    dm = 1
    df = 1.5
    fis.addInput([min_range, max_range], Name='left_sensor_value')
    fis.addMF('left_sensor_value', 'trapmf', [min_range, min_range, dn, dm], Name="CLOSE")
    fis.addMF('left_sensor_value', 'trapmf', [dn, dm, dm, df], Name="MEDIUM")
    fis.addMF('left_sensor_value', 'trapmf', [dm, df, max_range, max_range], Name="FAR")
    #fl.plotmf(fis, 'input', 0)
    fis.addInput([min_range, max_range], Name='middle_sensor_value')
    fis.addMF('middle_sensor_value', 'trapmf', [min_range, min_range, dn, dm], Name="CLOSE")
    fis.addMF('middle_sensor_value', 'trapmf', [dn, dm, dm, df], Name="MEDIUM")
    fis.addMF('middle_sensor_value', 'trapmf', [dm, df, max_range, max_range], Name="FAR")
    #fl.plotmf(fis, 'input', 1)
    fis.addInput([min_range, max_range], Name='right_sensor_value')
    fis.addMF('right_sensor_value', 'trapmf', [min_range, min_range, dn, dm], Name="CLOSE")
    fis.addMF('right_sensor_value', 'trapmf', [dn, dm, dm, df], Name="MEDIUM")
    fis.addMF('right_sensor_value', 'trapmf', [dm, df, max_range, max_range], Name="FAR")
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
    new_command = fl.evalfis(fis, list)
    interpreter(new_command)


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


def main():
    sensor_values = [generate_fake_reading() for _ in range(10)]
    print(sensor_values)
    for x in sensor_values:
        little_list = x
        print(little_list)
        fuzzy_controller(x)


if __name__ == '__main__':
    main()