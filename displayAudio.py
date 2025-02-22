import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

spf = wave.open("data.wav", "r")

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.frombuffer(signal, dtype=np.int16)

# If Stereo
if spf.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(signal)
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.show()
