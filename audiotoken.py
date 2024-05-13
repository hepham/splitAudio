import numpy as np
import matplotlib.pyplot as plt
import librosa

# Load the audio file
file_path = "your_audio_file_path.wav"  # Replace this with the path to your audio file
audio_signal, sample_rate = librosa.load(file_path, sr=None)

# Calculate the time axis
time = np.arange(0, len(audio_signal)) / sample_rate

# Plot the audio signal
plt.figure(figsize=(10, 4))
plt.plot(time, audio_signal, color='b')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Audio Signal')
plt.grid(True)
plt.show()
