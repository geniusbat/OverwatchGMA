#!/bin/bash
cd /home/OverwatchGMA
source .venv/bin/activate
echo -n " " > ips_to_ban
python3 nginx_manager.py test_nginx_rules
bash ./list_ban.sh
python3 nginx_manager.py clean_logs