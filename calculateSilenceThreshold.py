from pydub import AudioSegment
import numpy as np

def find_regions_below_average(audio_file, chunk_size=1000):
    audio = AudioSegment.from_file(audio_file)

    # Split audio into chunks
    chunks = [audio[i:i + chunk_size] for i in range(0, len(audio), chunk_size)]

    # Calculate RMS amplitude for each chunk
    amplitude = [np.sqrt(np.mean(np.array(chunk.get_array_of_samples())**2)) for chunk in chunks]

    # Find the average amplitude
    average_amplitude = np.mean(amplitude)

    # Find regions with amplitude below the average
    below_average_regions = []
    in_below_average_region = False

    for i, a in enumerate(amplitude):
        if a < average_amplitude:
            if not in_below_average_region:
                start_index = i
                in_below_average_region = True
        else:
            if in_below_average_region:
                end_index = i
                in_below_average_region = False
                below_average_regions.append((start_index * chunk_size, end_index * chunk_size))

    return below_average_regions

if __name__ == "__main__":
    audio_file_path = "data.wav"  # Thay thế bằng đường dẫn thực tế đến tệp audio của bạn

    # Tìm các khoảng có mức âm thanh dưới mức trung bình
    below_average_regions = find_regions_below_average(audio_file_path)

    for start, end in below_average_regions:
        print(f"Start Time: {start} ms, End Time: {end} ms")
