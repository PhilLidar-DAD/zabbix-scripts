#!/bin/bash

if [[ "$#" -ne 1 ]]; then
    echo "Specify configuration path! Exiting."
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

sed -i "s/<HOSTNAME>/$(hostname -s)/g" $1
sed -i "s/<SCRIPT_DIR>/${SCRIPT_DIR}/g" $1
