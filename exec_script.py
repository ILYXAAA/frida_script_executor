import os
with open('command.txt', 'r') as file:
    data = file.readlines()

os.system(f'{data[0]}')