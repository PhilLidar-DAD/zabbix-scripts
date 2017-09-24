#!/usr/bin/env python2

from pprint import pprint
import argparse
import os.path
import subprocess
import json
import logging

_version = '0.0.2'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
MAP_FILE = os.path.join(BASE_DIR, 'folder.map')

SCRIPTS_DIR =  '/mnt/misc/scripts/backup-scripts'
SIZETOBACKUP_DIR = os.path.join(SCRIPTS_DIR, 'sizetobackup')
TOTALSIZE_DIR = os.path.join(SCRIPTS_DIR, 'totalsize')

LOG_LEVEL = logging.DEBUG
CONS_LOG_LEVEL = logging.INFO
FILE_LOG_LEVEL = logging.DEBUG


def _parse_arguments():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version=_version)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('action', action='store',
                        choices=['discovery', 'sizetobackup', 'totalsize'])
    parser.add_argument('folder_name', nargs='?')
    args = parser.parse_args()
    return args


def _create_map_file():
    folder_map = {}
    out = subprocess.check_output(['ls', SIZETOBACKUP_DIR])
    for line in out.split('\n'):
        folder = line.strip()
        if folder:
            folder_map[folder] = folder
    json.dump(folder_map, open(MAP_FILE, 'w'), sort_keys=True, indent=4)


def _discovery():
    # Check if map file exists
    if not os.path.isfile(MAP_FILE):
        # Create map file
        _create_map_file()

    # Load disk map from file
    folder_map = json.load(open(MAP_FILE, 'r'))
    # pprint(folder_map)

    # Create JSON output
    data = []
    for k in folder_map.viewkeys():
        data.append({'{#FOLDER}': k})
    print json.dumps({'data': data}, sort_keys=True, indent=4)


def _sizetobackup(folder_name):
   # Check if map file exists
   if not os.path.isfile(MAP_FILE):
      # Create map file
      _create_map_file()
   # Load disk map from file
   folder_map = json.load(open(MAP_FILE, 'r'))
   folder = folder_map[folder_name]
   stb_file = open(os.path.join(SIZETOBACKUP_DIR,folder),'r')
   sizetobackup = stb_file.read()
   return sizetobackup

def _totalsize(folder_name):
   # Check if map file exists
   if not os.path.isfile(MAP_FILE):
      # Create map file
      _create_map_file()
   # Load disk map from file
   folder_map = json.load(open(MAP_FILE, 'r'))
   folder = folder_map[folder_name]
   ts_file = open(os.path.join(TOTALSIZE_DIR,folder),'r')
   totalsize = ts_file.read()
   return totalsize


if __name__ == '__main__':

    # Parse arguments
    args = _parse_arguments()

    if args.action == 'discovery':
        _discovery()
    elif args.action == 'sizetobackup':
        if not args.folder_name is None:
            print _sizetobackup(args.folder_name)
        else:
            print 'folder_name missing! Exiting.'
            exit(1)
    elif args.action == 'totalsize':
        if not args.folder_name is None:
            print _totalsize(args.folder_name)
        else:
            print 'folder_name missing! Exiting.'
            exit(1)
