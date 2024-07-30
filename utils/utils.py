import sys
sys.path.append("..")

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import re
from os import chdir, path

def parse_nginx_file(location):
    logs = []
    with open(location, 'r') as file:
        for line in file:
            logs.append(parse_nginx_log(line))
    return logs

def parse_nginx_log(rawLog):
    pattern = "(?P<remote_address>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (?P<user>.*|\s)- \[(?P<time>.*)\] \"(?P<request_type>.*)\" (?P<request_status>\d+) (?P<body_bytes_sent>\d+) \"(?P<referer>.*)\" \"(?P<agent_user>.*)\"$"#r"[(?P<time>.*)] \"(?P<request_type>.*)\" (?P<request_status>\d+) (?P<body_bytes_sent>\d+) \"(?P<referer>.*)\" \"(?P<agent_user>.*)\"$"
    comp = re.compile(pattern)
    for m in comp.finditer(rawLog):
        return m.groupdict()
    return None