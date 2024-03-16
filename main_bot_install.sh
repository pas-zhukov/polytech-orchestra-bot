#!/bin/bash


SERVICE_NAME="orchestra-main-bot"
INSTALL_PATH="/opt/polytech-orchestra-bot/"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}.service"
TARGET="main_bot.py"

# Remove old version
if [[ -d $SERVICE_PATH ]]; then
    echo "---"
    rm -v $SERVICE_PATH
fi

# Creating service in systemd

touch $SERVICE_PATH
exec 1> $SERVICE_PATH
echo "[Unit]"
echo "Description=Orchestra main bot"
echo ""
echo "[Service]"
echo "Type=simple"
echo "ExecStart=${INSTALL_PATH}/venv/bin/python3 ${INSTALL_PATH}${TARGET}"
echo "Restart=on-failure"
echo ""
echo "User=root"
echo "Group=root"
echo "[Install]"
echo "WantedBy=multi-user.target"


systemctl daemon-reload
systemctl enable ${SERVICE_NAME}.service
systemctl start ${SERVICE_NAME}.service