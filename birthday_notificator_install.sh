#!/bin/bash


SERVICE_NAME="orchestra-birthday-bot"
INSTALL_PATH="/opt/polytech-orchestra-bot/"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}.service"
TIMER_PATH="/etc/systemd/system/${SERVICE_NAME}.timer"
TARGET="birthday_notification_bot.py"

# Remove old version
if [[ -d $SERVICE_PATH ]]; then
    echo "---"
    rm -v $SERVICE_PATH
    rm -v $TIMER_PATH
fi

# Creating service in systemd

touch $SERVICE_PATH
# Fill .service file
exec 1> $SERVICE_PATH
echo "[Unit]"
echo "Description=Orchestra one-time birthday check bot"
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
echo "Description=Orchestra one-time birthday check bot"
echo ""
echo "[Timer]"
echo "OnCalendar=12:00:00"


systemctl daemon-reload
systemctl enable ${SERVICE_NAME}.service
systemctl enable ${SERVICE_NAME}.timer
systemctl start ${SERVICE_NAME}.timer