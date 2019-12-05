'''
Will Walker
University of Colorado Boulder
Creation Date:  Wednesday, December 4th 2019, 2:34:03 pm
File: testing_dict.py
'''
from tqdm import tqdm
from tqdm import trange
from psycopg2.extensions import QuotedString
from psycopg2.extensions import AsIs
from psycopg2 import sql
from obd import OBDStatus
import datetime
import string
import psycopg2
import obd
import sys
import os
sys.path.insert(
    0, os.path.realpath(os.path.dirname(__file__)))


command = []
test_dict = obd.commands.__dict__
# * column names
columns = ["time"]
# * column values
results = [datetime.datetime.now()]
# dictionary generation
for key, i in tqdm(test_dict.items(), desc="Generating Dictionary"):
    command.append((key, test_dict[key]))
description = []
with tqdm(desc="Running Commands", total=171) as pbar:
    temp2 = command[0][1][1]
    for i in range(3, 32):
        if(temp2[i] != 'None'):
            description.append(str(temp2[i]))
            pbar.update()
    for i in range(34, 64):
        if(temp2[i] != 'None'):
            description.append(str(temp2[i]))
            pbar.update()
    for i in range(66, len(temp2)):
        if(temp2[i] != 'None'):
            description.append(str(temp2[i]))
            pbar.update()
    temp2 = command[0][1][6]
    for i in range(1, 32):
        if(str(temp2[i]) != 'None'):
            description.append(str(temp2[i]))
            pbar.update()
    for i in range(33, 48):
        if(str(temp2[i]) != 'None'):
            description.append(str(temp2[i]))
            pbar.update()
    for i in range(49, 64):
        if(str(temp2[i]) != 'None'):
            description.append(str(temp2[i]))
            pbar.update()
    for i in range(65, 96):
        if(str(temp2[i]) != 'None'):
            description.append(str(temp2[i]))
            pbar.update()
    for i in range(97, 128):
        if(str(temp2[i]) != 'None'):
            description.append(str(temp2[i]))
            pbar.update()
    for i in range(129,160):
        if(str(temp2[i]) != 'None'):
            description.append(str(temp2[i]))
            pbar.update()
    for i in range(161,len(temp2)):
        if(str(temp2[i]) != 'None'):
            description.append(str(temp2[i]))
            pbar.update()
pbar.close()
print(len(description))
