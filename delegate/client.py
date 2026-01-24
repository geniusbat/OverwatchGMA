import requests, argparse, json, sys

class Client():
    server_url :str = ""
    port :int = ""
    https: bool = True
    token: str = ""
    session: requests.sessions.Session = None

    def __init__(self, server_url, token:str, port="", https=True):
        self.server_url = server_url
        #Reove slash if already ending in one
        if self.server_url[-1]=="/":
            self.server_url = self.server_url[:-1]
        self.port = port
        self.token = token
        self.https = https

        self.session = requests.sessions.Session()
        #self.session.keep_alive = False
    
    def _build_endpoint(self, api_endpoint, extra_args:list[str]=[])->str:
        protocol = "https://"
        if not self.https:
            protocol ="http://"
        port_endpoint = ""
        if self.port != "":
            port_endpoint = ":"+str(self.port)
        extras = ""
        if len(extra_args)>0:
            for extra in extra_args:
                extras += extra+"/"
        full_endpoint = "{protocol}{server_url}{port}/api/{api_endpoint}/{extras}".format(
            protocol=protocol,
            server_url=self.server_url,
            port = port_endpoint,
            api_endpoint = api_endpoint,
            extras=extras
        )
        return full_endpoint

    def _get_header_auth(self):
        return {'Authorization': 'Token {}'.format(self.token)}

    def _get_header_json_mediatype(self):
        return {'Content-type': 'application/json'}

    def options_delegate_controls(self):
        full_endpoint = self._build_endpoint("delegate_controls")
        response = self.session.options(full_endpoint, headers=self._get_header_auth())
        return response

    def post_delegate_controls(self, data:str):
        #Make sure data is json
        try:
            json.loads(data)
        except ValueError as e:
            raise e
        full_endpoint = self._build_endpoint("delegate_controls")
        headers = {}
        headers.update(self._get_header_auth())
        headers.update(self._get_header_json_mediatype())
        response = self.session.post(full_endpoint, data=data, headers=headers)
        return response

    def post_delegate_errors(self, data:str):
        #Make sure data is json
        try:
            json.loads(data)
        except ValueError as e:
            raise e
        full_endpoint = self._build_endpoint("delegate_errors")
        headers = {}
        headers.update(self._get_header_auth())
        headers.update(self._get_header_json_mediatype())
        response = self.session.post(full_endpoint, data=data, headers=headers)
        return response

    def close(self):
        self.session.close()
    
    def __str__(self):
        return "Client: {}:{}".format(self.server_url, self.port)
    
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test", help="(Optional) Ignores everything and tries to connect to localhost:8000", action="count", required=False)
    parser.add_argument("--url", help="Base url of the api", required=not '--test' in sys.argv)
    parser.add_argument("--token", help="Token to use for authentication", required=True)
    parser.add_argument("--port", help="(Optional) Port of the api (empty as default)", default="", required=False)
    parser.add_argument("--https", help="(Optional) Specify if requests should go through http or https (default)", default="true", required=False)
    args=parser.parse_args()
    #Test connection
    if args.test:
        print("TESTING")
        cl = Client("127.0.0.1",args.token,"8000",False,)
        response = cl.options_delegate_controls()
        #print(response)
    #Handle parameters passed
    else:
        #TODO: Handle creation of stuff and such
        pass

'''
ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

#Generate context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
#context.load_cert_chain(certfile="/home/phobos/Documents/Programing/OverwatchGMA/master/certs/cert.pem", keyfile="/home/phobos/Documents/Programing/OverwatchGMA/master/certs/key.pem")
#context.set_ciphers("@SECLEVEL=1:ALL")
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
ssocket = context.wrap_socket(ssocket)

print("TCP over SSL server running at https://0.0.0.0:8443")
ssocket.connect(('0.0.0.0', 8443))
ssocket.send(b"Hola mundo")
print(ssocket.recv(4096).decode())
import time
ssocket.close()
'''