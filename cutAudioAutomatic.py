from pydub import AudioSegment
from pydub.silence import split_on_silence

def split_audio_on_silence(audio_file, min_silence_len=1000, silence_thresh=-32):
    # Load the audio file
    audio = AudioSegment.from_file(audio_file)

    # Split audio on silence
    segments = split_on_silence(
        audio,
        min_silence_len=min_silence_len,     # minimum silence length in milliseconds
        silence_thresh=silence_thresh        # silence threshold in dBFS
    )

    return segments

if __name__ == "__main__":
    audio_file_path = "data.wav"  # Replace with the actual path to your audio file

    segments = split_audio_on_silence(audio_file_path)

    for i, segment in enumerate(segments):
        segment.export(f"segment_{i + 1}.wav", format="wav")
        print(f"Segment {i + 1} exported.")
