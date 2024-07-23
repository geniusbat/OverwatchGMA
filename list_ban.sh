#!/bin/bash
#Run chmod 777

# Path to the file containing the list of IPs to deny
DENY_IPS_FILE="ips_to_ban"

# Loop through each IP in the file and add a deny rule
while IFS= read -r ip; do
  # Check if the IP is already denied
  ufw status | grep -q "DENY IN from $ip"
  if [ $? -ne 0 ]; then
    # Deny the IP
    ufw insert 2 deny from "$ip"
  fi
done < "$DENY_IPS_FILE"

ufw reload