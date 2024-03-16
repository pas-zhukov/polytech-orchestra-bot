#!/bin/bash

INSTALL_PATH="/opt/polytech-orchestra-bot/"

#Check user rights
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

# shellcheck disable=SC2164
cd ${INSTALL_PATH}

# Creating venv and install python dependencies
apt install python3-virtualenv
virtualenv venv
./venv/bin/pip install -r requirements.txt

# Make scripts runnable
# chmod +x ./birthday_notificator_install.sh
# chmod +x ./whitehall_checker_install.sh

./birthday_notificator_install.sh
./whitehall_checker_install.sh


