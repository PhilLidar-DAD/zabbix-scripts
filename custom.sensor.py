#!/usr/bin/env python

import argparse
import json
import subprocess

from pprint import pprint
from collections import defaultdict


def parse_arguments():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('action', action='store', choices=['discovery', 'get'])
    parser.add_argument('item', nargs='?')
    args = parser.parse_args()
    return args


def discovery():
    data = []

    # Get data from sensors
    data += get_sensors_data()

    # Get data from ipmitool
    data += get_ipmitool_data()

    print json.dumps({'data': data}, sort_keys=True, indent=4)
    # print get_sensors_data('sensors-coretemp-isa-0001-Core_7')


def get_sensors_data(item=""):

    # Get sensors data
    sensors = subprocess.check_output(['sensors', '-u'])

    data = []
    sensor_data = {}
    device = ''
    for l in sensors.split('\n'):
        line = l.strip()
        if line and 'Adapter' not in line:  # Skip empty lines
            if ':' in line:
                tokens = line.split(':')
                # print('tokens:', tokens)
                if tokens[1]:
                    # If there is a 2nd token, there is a value
                    value = float(tokens[1].strip())

                    # Get mode
                    mode = tokens[0]
                    if ('average_interval' not in mode
                            and 'average' in mode
                            or 'input' in mode):
                        sensor_data['{#READING}'] = value

                        # Get units
                        if 'input' in mode:
                            sensor_data['{#UNITS}'] = 'C'
                        elif 'average' in mode:
                            sensor_data['{#UNITS}'] = 'W'

                        # Return value for specific sensor
                        if item == sensor_data['{#SENSOR}']:
                            print value
                            exit(0)
                    elif 'max' in mode:
                        sensor_data['{#UP_NONCRI}'] = value
                    elif 'crit' in mode and 'crit_alarm' not in mode:
                        sensor_data['{#UP_CRI}'] = value
                    # print 'sensor_data:', sensor_data
                else:
                    # If no 2nd token, this is a new sensor
                    if sensor_data:
                        data.append(sensor_data)
                    sensor = device + '-' + tokens[0]
                    sensor_data = {'{#SENSOR}': sensor.replace(' ', '_')}
            else:
                # New device if no ':' in line
                device = 'sensors-' + line
    if sensor_data:
        data.append(sensor_data)

    # pprint(data)
    return data


def get_ipmitool_data(item=""):

    # Get ipmitool data
    ipmitool = subprocess.check_output(['ipmitool', 'sensor'])

    data = []
    device = ''
    for l in ipmitool.split('\n'):
        line = l.strip()
        # Skip empty lines
        if not line:
            continue
        tokens = line.split('|')
        # print 'tokens:', tokens

        # Get sensor name
        sensor = 'ipmitool-' + tokens[0].strip().replace(' ', '_')
        # Get value
        if 'na' in tokens[1]:
            # Skip sensor
            continue
        elif '0x' in tokens[1]:
            value = int(tokens[1].strip(), 0)

            # Get thresholds
            lo_nonrec = lo_cri = lo_noncri = 1
            up_noncri = up_cri = up_nonrec = 1
        else:
            value = float(tokens[1].strip())

            # Get thresholds
            lo_nonrec = float(tokens[4].strip())
            lo_cri = float(tokens[5].strip())
            lo_noncri = float(tokens[6].strip())
            up_noncri = float(tokens[7].strip())
            up_cri = float(tokens[8].strip())
            up_nonrec = float(tokens[9].strip())

        # Return value for specific sensor
        if item == sensor:
            print value
            exit(0)

        # Get units
        if 'degrees C' in tokens[2]:
            units = 'C'
        elif 'Volts' in tokens[2]:
            units = 'V'
        else:
            units = tokens[2].strip()

        sensor_data = {
            '{#SENSOR}': sensor,
            '{#READING}': value,
            '{#UNITS}': units,
            '{#LO_NONREC}': lo_nonrec,
            '{#LO_CRI}': lo_cri,
            '{#LO_NONCRI}': lo_noncri,
            '{#UP_NONCRI}': up_noncri,
            '{#UP_CRI}': up_cri,
            '{#UP_NONREC}': up_nonrec
        }
        data.append(sensor_data)

    # pprint(data)
    return data


if __name__ == '__main__':

    # Parse arguments
    args = parse_arguments()

    if args.action == 'discovery':
        discovery()
    elif args.action == 'get':
        # print args.item
        get_sensors_data(args.item)
        get_ipmitool_data(args.item)
