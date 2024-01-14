from pydub import AudioSegment
import numpy as np

def calculate_auto_silence_threshold(audio_file, chunk_size=1000, percentile=10):
    audio = AudioSegment.from_file(audio_file)

    # Split audio into chunks
    chunks = [audio[i:i + chunk_size] for i in range(0, len(audio), chunk_size)]

    # Calculate RMS energy for each chunk
    energy = [np.sqrt(np.mean(np.array(chunk.get_array_of_samples())**2)) for chunk in chunks]

    # Calculate the threshold as the percentile of the energy
    silence_thresh = np.percentile(energy, percentile)

    return silence_thresh

if __name__ == "__main__":
    audio_file_path = "data.wav"  # Thay thế bằng đường dẫn thực tế đến tệp audio của bạn

    # Tính toán silence threshold tự động
    silence_thresh = calculate_auto_silence_threshold(audio_file_path)
    print(f"Auto-calculated silence threshold: {silence_thresh}")
