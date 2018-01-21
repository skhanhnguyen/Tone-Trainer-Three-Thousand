import audio_test
import numpy as np
from pymatbridge import Matlab
import pyaudio
import numpy
import scipy.io.wavfile as wav
import wave
import sys

#numpydata,recordseconds = audio_test.audio_to_nparray()



mlab = Matlab()
mlab.start()

res = mlab.run_func('pitchcontour2.m',{'arg1':np.array([numpydata]).transpose()})
