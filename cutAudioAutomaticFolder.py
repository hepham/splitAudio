import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import shutil

def split_audio_on_silence(audio_file, output_folder, min_silence_len=1000, silence_thresh=--29):
    try:
        audio = AudioSegment.from_file(audio_file)
        segments = split_on_silence(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh
        )
        return segments
    except Exception as e:
        print(f"Error: {e}")
        return []

def split_and_save_all_audio(input_folder, output_folder, min_silence_len=1000, silence_thresh=-32):
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            audio_file_path = os.path.join(input_folder, filename)
            segments = split_audio_on_silence(audio_file_path, output_folder, min_silence_len, silence_thresh)
            print(f"____________{filename}________________")
            if segments:
                audio_name = os.path.splitext(filename)[0]
                subfolder = os.path.join(output_folder, audio_name)
                os.makedirs(subfolder, exist_ok=True)
                shutil.copy(audio_file_path, subfolder)
                for i, segment in enumerate(segments):
                    output_file = os.path.join(subfolder, f"{i + 1}.wav")
                    segment.export(output_file, format="wav")
                    print(f" {i + 1}  exported to {output_file}")
            else:
                print(f"No segments found in {filename}.")

if __name__ == "__main__":
    input_folder_path = "input"
    output_folder_path = "output"

    split_and_save_all_audio(input_folder_path, output_folder_path)
