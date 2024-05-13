import librosa

# Load the audio file
file_path = "D:\Project\Python\SplitAudio\output\Voice 001\1.wav"  # Replace this with the path to your audio file
audio_signal, sample_rate = librosa.load(file_path, sr=None)

# Set a threshold for silence detection
threshold = 0.01  # Adjust as needed

# Find the index where the audio signal rises above the threshold
start_index = next((i for i, x in enumerate(audio_signal) if abs(x) > threshold), None)

# If there was silence at the beginning, trim the audio signal
if start_index is not None:
    audio_signal_trimmed = audio_signal[start_index:]

    # Optionally, save the trimmed audio signal to a new file
    trimmed_file_path = "trimmed_audio_file.wav"
    librosa.output.write_wav(trimmed_file_path, audio_signal_trimmed, sample_rate)
    print("Trimmed audio saved to:", trimmed_file_path)
else:
    print("No silence found at the beginning of the audio.")
