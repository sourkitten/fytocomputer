#! /usr/bin/bash

# Check if the script is being run as root
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run as root."
  exit 1
fi

pip install requests socket
mkdir -p /home/grafana/ip-alert/
cp ip-alert.py /home/grafana/ip-alert/

echo "[Unit]
Description=Starts the ip alert system

[Service]
ExecStart=/usr/bin/python3 /home/grafana/ip-alert/ip-alert.py
Type=simple
" > /lib/systemd/system/ip-alert.service
systemctl daemon-reload
systemctl enable ip-alert.service
systemctl start ip-alert.service

chown -R grafana:grafana /home/grafana/ip-alert/
chmod -R g+rwx /home/grafana/ip-alert/
