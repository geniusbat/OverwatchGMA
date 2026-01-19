Run server (old version)
python master/server.py --cert_key master/certs/key.pem --cert_file master/certs/cert.pem --log_file master/logs.log


IMPORTANT:
-Remember that API tokens are in plaintext when in http, so either use VPN or https when connecting from delegate to server!