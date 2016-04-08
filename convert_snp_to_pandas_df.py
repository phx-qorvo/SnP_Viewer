from read_touchstone import Touchstone
import pandas as pd
import numpy as np
from Tkinter import *
import os
from UI_file_select import UserInterface


# file = './Data/A.s3p'   

def convert_snp_csv(file):
    fpn_split = file.split('.')
    f_ext = fpn_split[-1]  # file extension         
    # if f_ext =='s2p':                        
    Instance = Touchstone(file)
    freq, array = Instance.get_sparameter_arrays()
    names = Instance.get_sparameter_names()
    s11 = array[:, 0, 0]
    sParams = pd.DataFrame(columns=names)

    strings = []
    for i, name in enumerate(names):
        if i == 0:
            sParams[str(name)] = freq
        else:
            # S11 is indexs 00 and s21 is indexs 10 etc..
            if 'R' in name:
                sParams[name] = np.real(
                    array[:, int(name[1]) - 1, int(name[2]) - 1])
            if 'I' in name:
                sParams[name] = np.imag(
                    array[:, int(name[1]) - 1, int(name[2]) - 1])

    head, tail = os.path.split(file)
    filename, file_extension = os.path.splitext(tail)

    # calculate mag_phase (goes up to 20 port, but can easily add more)
    for x in range(0, 20):
        for y in range(0, 20):
            if 'S' + str(x) + str(y) + 'R' in sParams.columns:
                complex = sParams['S' + str(x) + str(y) + 'R'] + \
                          sParams['S' + str(x) + str(y) + 'I'] * 1j

                sParams['S' + str(x) + str(y) + '_Mag'] = 20 * np.log10(
                    np.absolute(complex))

                sParams['S' + str(x) + str(y) + '_Ang'] = np.angle(complex,
                                                                   deg=True)

    bandsearch = False  # CONTORL
    # Extract Band From Filename
    if bandsearch == True:
        band = ''
        for x, letter in enumerate(filename):
            if letter == 'B' or letter == 'b':
                try:
                    value = int(tail[x + 1])
                    band += str(letter)
                    band += str(tail[x + 1])
                except ValueError:
                    pass
                try:
                    value = int(tail[x + 2])
                    band += str(value)
                except ValueError:
                    pass
                if tail[x + 3] == 'a' or tail[x + 3] == 'A' or \
                                tail[x + 3] == 'b' or tail[x + 3] == 'B':
                    band += str(tail[x + 3])
                sParams['band'] = str(band)

    # More Calculated columns
    sParams['sourcefile'] = filename
    sParams['MHz'] = sParams['frequency'] * (1 / 1e6)
    sParams = sParams.drop('frequency', 1)

    sParams.to_csv('./Data/output/' + filename + '.csv', index=False)
    return sParams
