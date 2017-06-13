#!/usr/bin/env python

import argparse
import json
import subprocess


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

    # Get data from ipmitool

    print json.dumps({'data': data}, sort_keys=True, indent=4)


def parse_sensors(item=""):

    # Get sensors data
    sensors = subprocess.check_output(['sensors', '-u'])

    for l in sensors.split('\n'):
        line = l.strip()

if __name__ == '__main__':

    # Parse arguments
    args = parse_arguments()

    if args.action == 'discovery':
        pass
    elif args.action == 'get':
        pass
