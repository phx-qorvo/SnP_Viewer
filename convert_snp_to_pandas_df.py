from read_touchstone import Touchstone
import pandas as pd
import numpy as np
import os
import re


def convert_snp_csv(file):
    Instance = Touchstone(file)
    freq, array = Instance.get_sparameter_arrays()
    names = Instance.get_sparameter_names()
    sParams = pd.DataFrame(columns=names)

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

                sParams['S' + str(x) + str(y) + '_dB'] = 20 * np.log10(
                    np.absolute(complex))

                sParams['S' + str(x) + str(y) + '_Ang'] = np.angle(complex, deg=True)

    # More Calculated columns
    sParams['sourcefile'] = filename
    sParams['Frequency'] = sParams['frequency'] * (1 / 1e6)
    sParams = sParams.drop('frequency', 1)
    num = [int(s) for s in re.findall(r'\d+', file_extension)]  # get file extension
    sParams['order'] = num[0]
    #move Frequency to be the first column
    columns = list(sParams.columns.values)
    columns.insert(0,columns.pop(columns.index('Frequency')))
    sParams = sParams[columns]
    return sParams
