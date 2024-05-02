from ui import main_window
from PyQt5 import QtWidgets
import sys
import os
from os import system as send
from launch_adb import launch_adb_server
import configparser
from main_js_maker import make_trace_methods_script
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog

class SSL_unpinning_app(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        self.device_ip = self.config["DEVICE"]["DEVICE_IP"]
        self.device_port = self.config["DEVICE"]["DEVICE_PORT"]
        self.lineEdit_ip.setText(self.device_ip)
        self.lineEdit_port.setText(self.device_port)

        self.pushButton_launch_adb.clicked.connect(self.launch_adb)
        self.pushButton_kill_adb_server.clicked.connect(self.kill_adb)
        self.pushButton_choose_apk.clicked.connect(self.choose_apk_for_js_script)
        self.pushButton_generate_trace_script.clicked.connect(self.generate_trace_script)
        self.pushButton_save_settings.clicked.connect(self.save_settings)
        self.pushButton_exec_script_2.clicked.connect(self.update_scripts_list)

        self.pushButton_exec_script.clicked.connect(self.exec_script)
        self.scripts_list = os.listdir("scripts")
        self.app_source_list = []
        self.app_name_list = []
        self.step = 0
        #os.chdir('platform-tools')

    def update_scripts_list(self):
        self.scripts_list = os.listdir("scripts")
        self.comboBox_script.clear()
        self.comboBox_script.addItems(self.scripts_list)

    def save_settings(self):
        new_ip = self.lineEdit_ip.text()
        new_port = self.lineEdit_port.text()
        self.config.set('DEVICE', 'DEVICE_IP', new_ip)
        self.config.set('DEVICE', 'DEVICE_PORT', new_port)

        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)
        
        msg = QMessageBox() 
        msg.setIcon(QMessageBox.Information) 
        msg.setText("Настройки сохранены") 
        msg.setWindowTitle("Информация") 
        msg.setStandardButtons(QMessageBox.Ok) 
        retval = msg.exec_() 

    def launch_adb(self):
        self.comboBox_script.clear()
        self.comboBox_script.addItems(self.scripts_list)
        launch_adb_server(self.device_ip, self.device_port)
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
    
    def choose_apk_for_js_script(self):
        file_dialog = QFileDialog()
        file_path = file_dialog.getOpenFileName(None, "Выберите файл", "", "Apk(*.apk);;All Files (*.*)")[0]
        self.lineEdit_apk_file.setText(file_path)
    
    def generate_trace_script(self):
        if os.path.exists(self.lineEdit_apk_file.text()):
            result = make_trace_methods_script(self.lineEdit_apk_file.text())
            if not result:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Что-то пошло не так во время декомпиляции!')
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Такого файла не существует!')
            msg.setWindowTitle("Error")
            msg.exec_()


    def kill_adb(self):
        os.chdir("platform-tools")
        send(f'echo adb kill-server')
        send('adb kill-server')
        send(f'echo ### adb server stopped ###')
        os.chdir("..")
        self.step = 0

    def exec_script(self):
        for i in range(len(self.app_name_list)):
            if self.app_name_list[i] == self.comboBox_app.currentText():
                app = self.app_source_list[i]
                break
        self.plainTextEdit_logs.setPlainText(self.plainTextEdit_logs.toPlainText() + f'frida -U -l "{self.comboBox_script.currentText()}" -f {app}' + '\n')
        with open('command.txt', 'w') as file:
            file.write(f'frida -U -l "scripts/{self.comboBox_script.currentText()}" -f {app}')
        os.startfile('exec_script.py')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SSL_unpinning_app()
    window.show()
    app.exec_()