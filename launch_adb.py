import os
import keyboard
import pyperclip
import time
from os import system as send
def launch_adb_server():
    send('echo ### Exec connection ### ')
    send('adb connect 127.0.0.1:21503')
    send('echo ### Devices List: ###')
    send('adb devices')
    send('echo ### Pushing Frida Server: ###')
    send('adb push frida-server /data/local/tmp')
    send('adb shell chmod 777 /data/local/tmp/frida-server')
    send('echo ### Pushing Certificates: ###')
    send('adb push cacert.crt /data/local/tmp')
    send('adb shell chmod 777 /data/local/tmp/cacert.crt')
    send(f'echo ### Pushing Scripts: ###')
    scripts_list = os.listdir("scripts")
    for script in scripts_list:
        send(f'adb push scripts/{script} /data/local/tmp')
    send(f'echo ### All commands were executed ###')

    os.startfile('cmd.exe')
    time.sleep(3)
    pyperclip.copy('adb shell /data/local/tmp/frida-server &')
    keyboard.send('CTRL+V')
    time.sleep(0.1)
    keyboard.send('ENTER')