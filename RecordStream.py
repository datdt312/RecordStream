# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 18:41:42 2020

@author: Hope
"""

import numpy as np
import sounddevice as sd
import soundfile as sf
import time
import queue

sd.default.device = 0
_FS = 16000
_CHANNELS = 1

q = queue.Queue()
link = ''
records = []

def addRecord(filename, data, text):
    records.append([filename, data, text])
    
def saveRecord(name):
    fname = 'result-data-' + name
    f = open(fname, 'w', encoding='utf-8')
    resultData = []
    resultData.append(link)
    
    for r in records:
        sf.write(r[0],r[1],_FS) # r[0]: filename , r[1]: data
        resultData.append(str(r[0])) # r[0]: filename
        resultData.append(str(r[2])) # r[2]: text
    
    f.write('\n'.join(resultData))
    f.close()
    print('Save All Data Successfully')
    
def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status)
    q.put(indata.copy())

def recordstream(text):
    try:
        data = []
        with sd.InputStream(samplerate=_FS,
                       channels=_CHANNELS,
                       callback=audio_callback) as stream:
            print('Recording . . .')
            print('Press Ctrl + C to stop recording!')
            while True:                    
                data = np.append(data, q.get())
            
    except KeyboardInterrupt:
       print('Stop recording')
       filename = input('Enter filename to save record: ')
       addRecord(filename + '.wav',data, text)
       #sf.write(filename + '.wav', data, _FS)
       print('Save successfully')

def readDataFile(file):
    # =============================================================================
    #   ------ file format ------
    #   line 1: link bài báo
    #   lines : các dữ liệu bài báo
    # =============================================================================
    f = open(file,'r', encoding='utf-8')
    link = f.readline()[:-1]
    contents = f.read().split('\n')
    
    return link, contents

def showText(text):
    print('#'*50 + '\n')
    print('\t' + text)
    print('\n'+'#'*50)
  
def main(filename):
    #filename = 'thoi-su.txt'
    globals()['link'], contents = readDataFile(filename)
    print('Read data successfully!\n')
    cin = input('start recording? [Y/N]: ')
    if (cin.lower()=='y'):
        globals()['record'] = []
        globals()['q'].queue.clear()
        for text in contents:
            print('-- ' + str(contents.index(text)) + ' --')
            showText(text)
            if (input('record this sentence? [Y/N]: ').lower()=='y'):
                recordstream(text)
            if (input('next sentence?[Y/N]:').lower()=='n'):
                break;
        print('------------End------------')
        saveRecord(filename)
    else: 
        return
    
def program(filename):
    globals()['record'] = []
    globals()['q'].queue.clear()
    while True:
      main(filename)
      off = input('Turn off the program? [Y/N]: ')
      if (off.lower()=='y'):
          break

