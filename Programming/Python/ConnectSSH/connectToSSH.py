import paramiko
from paramiko import SSHClient
# from scp import SCPClient
import time 

class connectToSSH():
    def __init__(self, IPAdress, host, PWD):
        self._host = host
        self._IP = IPAdress
        self._pwd = PWD

        self._client = SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self._firstInit = True

    def connect(self): 
        print("Connecting to: {}".format(self._IP))
        
        try:
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(hostname = self._IP, username = self._host, password = self._pwd, allow_agent = False, look_for_keys = False)
            
            print("Connecting... SUCCESS!")

            self.startStream()
            return True

        except: 
            print("Connecting... FAILED!")
            return False
    def disconnect(self): 
        print("Disconnecting from {}".format(self._IP))
        self._client.close()
        print("Disconnection... SUCCESS!")
        return False

    def startStream(self):
        print("Starting stream")
        if(self._firstInit == True): 
            try: 
                self._client.exec_command("sudo vcdbg set awb_mode 0")
                
                # self._client.exec_command("raspistill -o test.jpg")
                time.sleep(2) #Waiting for command to execute
                print(self._client.exec_command("python3 src/client.py"))
                print("Red tint fixed")
                self._firstInit = False
            except: 
                print("Red tint adjustment failed")
                return

        try: 
            
            print("Stream started successfully")
        except: 
            print("Failed to start stream")