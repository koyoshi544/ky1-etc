import os
import datetime
# import pandas as pd

_env = os.environ

def main():  
    file_name = './TestData02.txt'
    nama_data = input_file(file_name)
    s6_data = split_data(nama_data)
    print(nama_data)
    print(s6_data)

def split_data(n_data):
    split_data = n_data.split()
    if (len(split_data) < 6):
         split_data.extend(['', '', '', '', '', ''])
    return split_data[0:6]
     
def input_file(f_name):
    rtn_data = ''
    with open(f_name, mode='r', encoding='utf-8') as f:
        rtn_data = f.read()
    return rtn_data

if __name__ == '__main__':  
    main()
