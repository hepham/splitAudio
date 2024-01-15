from pydub import AudioSegment
def merge_audio(file1_path, file2_path, output_path):
    # Load audio files
    audio1 = AudioSegment.from_file(file1_path)
    audio2 = AudioSegment.from_file(file2_path)

    # Concatenate the two audio files
    merged_audio = audio1 + audio2

    # Export the merged audio to a new file
    merged_audio.export(output_path, format="wav")  # You can change the format if needed

# Example usage
file1_path = "output/data/meger.wav"
file2_path = "output/data/3.wav"
output_path = "meger2.wav"

merge_audio(file1_path, file2_path, output_path)