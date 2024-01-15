import librosa
import numpy as np

def detect_silence(audio_path, threshold=0.001, duration_threshold=0.5):
    # Load audio file
    y, sr = librosa.load(audio_path)

    # Compute energy of the audio
    energy = np.sum(np.square(y))

    # Normalize energy by the length of the audio
    energy /= len(y)

    # Check if the energy is below the threshold
    if energy < threshold:
        print("Silence detected")

        # Check if the duration of silence is above the duration threshold
        duration = librosa.get_duration(y=y, sr=sr)
        if duration > duration_threshold:
            print(f"Silence duration: {duration} seconds")
        else:
            print("Silence duration below threshold")

    else:
        print("No silence detected")

# Example usage
audio_file_path = "data.wav"
detect_silence(audio_file_path)
