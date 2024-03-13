#!/bin/bash


INSTALL_PATH="/opt/polytech-orchestra-bot/"
SERVICE_PATH="/etc/systemd/system/orchestra-bot-schedule.service"
TIMER_PATH="/etc/systemd/system/orchestra-bot-schedule.timer"
TARGET="rehearsal_scheduled_bot.py"

# shellcheck disable=SC2164
cd ${INSTALL_PATH}

# Creating venv and install python dependencies
apt install python3-virtualenv
virtualenv venv
./venv/bin/pip install -r requirements.txt

#Check user rights
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

#Remove old version
if [[ -d $SERVICE_PATH ]]; then
    echo "---"
    # rm -rfv $INSTALL_PATH
    # rm  -v $CONFIGURATION
    rm -v $SERVICE_PATH
    rm -v $TIMER_PATH
fi

# Creating service in systemd

touch $SERVICE_PATH
# Fill .service file
exec 1> $SERVICE_PATH
echo "[Unit]"
echo "Description=Orchestra one-time schedule check bot"
echo ""
echo "[Service]"
echo "Type=oneshot"
echo "ExecStart=${INSTALL_PATH}/venv/bin/python3 ${INSTALL_PATH}${TARGET}"
echo ""
echo "User=root"
echo "Group=root"
echo "[Install]"
echo "WantedBy=multi-user.target"

touch $TIMER_PATH
# Fill .timer file
exec 1> $TIMER_PATH
echo "[Unit]"
echo "Description=Orchestra one-time schedule check bot"
echo ""
echo "[Timer]"
echo "OnCalendar=Mon,Fri *-09..12,01..05-* 15:*:*"
echo ""
echo "[Install]"
echo "WantedBy=timers.target"



systemctl daemon-reload
systemctl enable pk_metrics.service


