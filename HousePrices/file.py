#*************************************************************************************
# Date:     2021/02/11
# Objetive: Handle opeations with files
#*************************************************************************************
import os.path

from os import path

#*************************************************************************************
# Global variables
#*************************************************************************************
# Program Name
program_name = 'file.py'

class file():
    #*************************************************************************************
    # file_name:    the file name with extension
    #*************************************************************************************
    def __init__(self, file_name):
        self.file_name = file_name

    #*************************************************************************************
    # Name:         val_file
    # Description:  validate existence of a file
    # return:       exist - boolean that indicate the existence
    #*************************************************************************************
    def val_file(self):
        exist = False
        try:
            exist = path.exists(self.file_name)
        except Exception as e:
            print(20, program_name, "Error val_file:", e)
        return exist

    #*************************************************************************************
    # Name:         write_file
    # Description:  write lines into a file
    #*************************************************************************************
    def write_file(self, info_list = []):
        try:
            # Open file in write mode
            f = open(self.file_name,'w', encoding='utf-8')
            # Write lines into the file
            for l_list in info_list:
                f.write(l_list + '\n')
        except Exception as e:
            print(10, program_name, "Error write_file:", e)

    #*************************************************************************************
    # Name:         read_file
    # Description:  extract the lines from a file
    # return:       info_list - list with lines from a file
    #*************************************************************************************
    def read_file(self):
        info_list = []
        try:
            # Open file in read mode
            f = open(self.file_name,'r', encoding='utf-8')
            # Read all the lines
            lines = f.readlines()
            # Save lines into a list
            for l in lines:
                info_list.append(l.strip())
        except:
            self.write_file()
        return info_list