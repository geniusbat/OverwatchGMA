#!/bin/bash
cd /home/OverwatchGMA
source .venv/bin/activate
python3 nginx_manager.py test_nginx_rules
bash ./list_ban
python3 nginx_manager.py clean_logs