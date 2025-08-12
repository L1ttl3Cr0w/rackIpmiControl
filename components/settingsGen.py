from components.sendDB import collection
import configparser
import os
import time

class Settings:
    def __init__(self, fan_speed: int, mongoDB: bool, high_temp_threshold: int, low_temp_threshold: int, high_combined_threshold: int, low_combined_threshold: int):
        self.fan_speed = fan_speed
        self.mongoDB = mongoDB
        self.high_temp = high_temp_threshold
        self.low_temp = low_temp_threshold
        self.high_combined = high_combined_threshold
        self.low_combined = low_combined_threshold
        self.gpu_installed = False
        self.gen_structure = configparser.ConfigParser()
        self.path = 'example.ini'
    def generate_settings(self):
        self.gen_structure['Default'] = {
            'fan_speed': self.fan_speed,
            'gpu_installed': self.gpu_installed,
            'mongoDB': self.mongoDB
            }
        self.gen_structure['Temp_Parameters'] = {
            'high_temp_threshold': self.high_temp,
            'low_temp_threshold': self.low_temp,
            'high_combined_temp': self.high_combined,
            'low_combined_temp': self.low_combined
            }
        if os.path.isfile(self.path) is False:
            with open(f'{self.path}', 'w') as configfile:
                self.gen_structure.write(configfile)
                print('Done sleeping again for 2 seconds')
        elif os.path.isfile(self.path):
            print('File already exists, not creating a new one')
            regen_settings_file(input_settings('Regen of settings.ini', bool), self.path, self.gen_structure)
        else:
            print('Failure in file creation, non boolean value has been obtained')

def regen_settings_file(boolean, path, gen_structure):
    if boolean:
        with open(f'{path}', 'w') as configfile:
            gen_structure.write(configfile)
            print('file updated')
    else:
            print("File not updated")

def input_settings(parameter, input_type):
    if input_type == int:
        while True:
            try:
                value = int(input(f'{parameter}: '))
                if value > 100 or value < 0:
                    print("Value entered is either over 100 or entered lower than 0, please enter again.")
                    input_settings(parameter, input_type)
                return value
            except Exception as e:
                print("Entered value is not a number, please enter again.")
    elif input_type == bool:
        while True:
            try:
                return {'true':True, 'yes':True, 'false':False, 'no':False}[input(f'Activate {parameter}? (yes/no): ').lower()]
            except Exception as e:
                print(f'Please choose either yes/no or true/false.')
    else:
        return None
    
'''
collection.find_one_and_update({"_id": 0}, {"$set": {
    "settings": default
}})
'''