#!/usr/bin/env python2

from pprint import pprint
import argparse
import os.path
import subprocess
import json

_version = '0.1.24'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
MAP_FILE = os.path.join(BASE_DIR, 'disk.map')


def _parse_arguments():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version=_version)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('action', action='store',
                        choices=['discovery', 'temp'])
    parser.add_argument('disk_name', nargs='?')
    args = parser.parse_args()
    return args


def _create_map_file():
    disk_map = {}
    out = subprocess.check_output('ls /dev/da* | grep -v p', shell=True)
    for line in out.split('\n'):
        disk = line.strip()
        if disk:
            # print disk
            # Get model and serial no.
            out2 = subprocess.check_output(['smartctl', '-i', disk])
            model = None
            for line2 in out2.split('\n'):
                if 'device model:' in line2.lower():
                    model = line2.strip().split(':')[1].strip()
                elif 'serial number:' in line2.lower():
                    sn = line2.strip().split(':')[1].strip()
                elif 'vendor:' in line2.lower():
                    vendor = line2.strip().split(':')[1].strip()
                elif 'product:' in line2.lower():
                    product = line2.strip().split(':')[1].strip()
            if model:
                name = model.replace(' ', '_') + '_' + sn
            else:
                name = vendor + '_' + product + '_' + sn
            disk_map[name] = disk
    json.dump(disk_map, open(MAP_FILE, 'w'), sort_keys=True, indent=4)


def _discovery():
    # Check if map file exists
    if not os.path.isfile(MAP_FILE):
        # Create map file
        _create_map_file()

    # Load disk map from file
    disk_map = json.load(open(MAP_FILE, 'r'))
    # pprint(disk_map)

    # Create JSON output
    data = []
    for k in disk_map.viewkeys():
        data.append({'{#DISK_ID}': k})
    print json.dumps({'data': data}, sort_keys=True, indent=4)


def _temp(disk_name):
    while True:
        # Check if map file exists
        if not os.path.isfile(MAP_FILE):
            # Create map file
            _create_map_file()

        # Load disk map from file
        disk_map = json.load(open(MAP_FILE, 'r'))

        disk = disk_map[disk_name]

        # Get mode, serial no. & temperature
        try:
            out = subprocess.check_output(['smartctl', '-a', disk],
                                          stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError, e:
            # print 'Error getting temperature!'
            # print 'e.output:', e.output
            # print 'out:', out
            # exit(1)
            out = e.output
        model = None
        for line in out.split('\n'):
            if 'device model:' in line.lower():
                model = line.strip().split(':')[1].strip()
            elif 'serial number:' in line.lower():
                sn = line.strip().split(':')[1].strip()
            elif 'vendor:' in line.lower():
                vendor = line.strip().split(':')[1].strip()
            elif 'product:' in line.lower():
                product = line.strip().split(':')[1].strip()
            elif 'current drive temperature:' in line.lower():
                temp = int(line.strip().split(':')[1].strip().split()[0])
            elif 'Temperature_Celsius' in line:
                try:
                    temp = int(line.strip().split()[9])
                except ValueError:
                    print 'line:', line
                    print 'temp:', line.strip().split()[9]
                    return -1
        if model:
            name = model.replace(' ', '_') + '_' + sn
        else:
            name = vendor + '_' + product + '_' + sn
        if name != disk_name:
            # Recreate disk map
            os.remove(MAP_FILE)
            continue

        return temp

if __name__ == '__main__':

    # Parse arguments
    args = _parse_arguments()

    if args.action == 'discovery':
        _discovery()
    elif args.action == 'temp':
        if not args.disk_name is None:
            print _temp(args.disk_name)
        else:
            print 'disk_name missing! Exiting.'
            exit(1)
