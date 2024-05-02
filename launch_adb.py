import os
import keyboard
import pyperclip
import time
from os import system as send
def launch_adb_server(ip, port):
    os.chdir("platform-tools")
    send('echo ### Exec connection ### ')
    send(f'adb connect {ip}:{port}') #21503 - MEmu; 62001 - Nox Player
    send('echo ### Devices List: ###')
    send('adb devices')
    send('echo ### Pushing Frida Server: ###')
    send('adb push frida-server /data/local/tmp')
    send('adb shell chmod 777 /data/local/tmp/frida-server')
    send('echo ### Pushing Certificates: ###')
    send('adb push cacert.crt /data/local/tmp')
    send('adb shell chmod 777 /data/local/tmp/cacert.crt')
    send(f'echo ### Pushing Scripts: ###')
    os.chdir("..")
    scripts_list = os.listdir("scripts")
    
    current_path = os.path.dirname(os.path.realpath(__file__))
    scripts_path = os.path.join(current_path, "scripts")
    os.chdir("platform-tools")
    for script in scripts_list:
        path_to_script = os.path.join(scripts_path, script)
        send(f'adb push "{path_to_script}" /data/local/tmp')
    send(f'echo ### All commands were executed ###')

    os.startfile('cmd.exe')
    time.sleep(3)
    pyperclip.copy('adb shell /data/local/tmp/frida-server &')
    keyboard.send('CTRL+V')
    time.sleep(0.1)
    keyboard.send('ENTER')
    os.chdir("..")