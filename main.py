from ui import main_window
from PyQt5 import QtWidgets
import sys
import os
from os import system as send
from launch_adb import launch_adb_server

class Script_Executor(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_launch_adb.clicked.connect(self.launch_adb)
        self.pushButton_kill_adb_server.clicked.connect(self.kill_adb)
        os.chdir('platform-tools')
        self.pushButton_exec_script.clicked.connect(self.exec_script)
        self.pushButton_reload_scripts.clicked.connect(self.reload_scripts)
        self.scripts_list = os.listdir("scripts")
        self.app_source_list = []
        self.app_name_list = []
        self.step = 0

    def launch_adb(self):
        self.comboBox_script.clear()
        self.comboBox_script.addItems(self.scripts_list)
        launch_adb_server()
        self.plainTextEdit_logs.setPlainText('### ADB server was executed' + '\n')
        self.plainTextEdit_logs.setPlainText(self.plainTextEdit_logs.toPlainText() + '### All scripts pushed' + '\n')
        os.system('frida-ps -Uai' + ' > output.txt')

        self.plainTextEdit_logs.setPlainText(self.plainTextEdit_logs.toPlainText() + '### All apps: ' + '\n' + '\n')
        if os.path.exists('output.txt'):
            with open('output.txt', 'r') as file:
                data = file.readlines()

            data = data[2:len(data) - 1]

            new_data = []
            for i in range(len(data)):
                new_data.append(data[i].split())

            for i in range(len(new_data)):
                self.app_source_list.append(new_data[i][len(new_data[i]) - 1])

            for i in range(len(new_data)):
                self.app_name_list.append(new_data[i][len(new_data[i]) - 2])

            for i in range(len(self.app_name_list)):
                self.plainTextEdit_logs.setPlainText(
                    self.plainTextEdit_logs.toPlainText() + f'{self.app_name_list[i]} : {self.app_source_list[i]}' + '\n')
            self.comboBox_app.addItems(self.app_name_list)

            os.remove('output.txt')


    def kill_adb(self):
        send(f'echo adb kill-server')
        send('adb kill-server')
        send(f'echo ### adb server stopped ###')
        self.step = 0

    def exec_script(self):
        for i in range(len(self.app_name_list)):
            if self.app_name_list[i] == self.comboBox_app.currentText():
                app = self.app_source_list[i]
                break
        self.plainTextEdit_logs.setPlainText(self.plainTextEdit_logs.toPlainText() + f'frida -U -l {self.comboBox_script.currentText()} -f {app}' + '\n')
        with open('command.txt', 'w') as file:
            file.write(f'frida -U -l scripts/{self.comboBox_script.currentText()} -f {app}')
        os.startfile('exec_script.py')

    def reload_scripts(self):
        self.scripts_list = os.listdir("scripts")
        self.comboBox_script.clear()
        self.comboBox_script.addItems(self.scripts_list)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Script_Executor()
    window.show()
    app.exec_()
