#from paramiko import SSHClient
import paramiko
from paramiko import SSHClient
from scp import SCPClient
import time 
import os

class getImageClass(): 
    def __init__(self, imageWidth, imageHeight, returnPath, IPAdress, PWD, imageDir):
        print("Initiating Image class")

        self._width = imageWidth
        self._height = imageHeight
        self._rPath = returnPath
        self._IP = IPAdress
        self._pwd = PWD
        self.iDir = imageDir

        print("Image class initiated successfully") 
        self._client = SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    def connectToNetwork(self): 
        print("Connecting to: {}".format(self._IP))
        
        try:
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(hostname = self._IP, username = "pi", password = self._pwd, allow_agent = False, look_for_keys = False)
            
            print("Connecting... SUCCESS!")
            return True

        except: 
            print("Connecting... FAILED!")
            return False
    def disconnect(self): 
        print("Disconnecting from {}".format(self._IP))
        self._client.close()
        print("Disconnection... SUCCESS!")
        return False

    def sendImage(self):
        # sftp = self._client.open_sftp()   
        # sftp.chdir("/src")
        # print(sftp.listdir())
        # sftp.chdir('src')
        scp = SCPClient(self._client.get_transport())
        scp.get(remote_path = "/home/pi/src/test.png", local_path = "/Users/Philip/Documents/Programming/SCARA-Robotic-Arm/Programming/Python/GetImage/img")
        scp.close()
        # sftp.put("test.png", "/home/pi/src/")
        # sftp.close()/Users/Philip/Desktop/abc
        try: 
            pass
        except: 
            print("Failed")
    def captureImage(self):
        try: 
            while(1):
                print(self._client.exec_command("libcamera-still -o ~/src/test.png"))
            time.sleep(10)
            print("Image Captured")
        except: 
            print("Failed to capture image")