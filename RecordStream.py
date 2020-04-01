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

def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status)
    q.put(indata.copy())

def split_track(data, track): 
    print('splitting')
    data.append(track)
    track = []
    print('Split track_' + str(len(data)))
    
def recordstream():
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
       sf.write(filename + '.wav', data, _FS)
       print('Save successfully')
  
def main():
    cin = input('start recording? [Y/N]: ')
    if (cin.lower()=='y'):
        q.queue.clear()
        recordstream()
    else: 
        return
    
       
if __name__ == '__main__':
     while True:
        main()
        off = input('Turn off the program? [Y/N]: ')
        if (off.lower()=='y'):
            break

