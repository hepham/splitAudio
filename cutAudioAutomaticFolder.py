import itertools
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent
import shutil
import speech_recognition as sr

def split_on_silence(audio_segment, min_silence_len=1000, silence_thresh=-16,duration=20, keep_silence=100,
                     seek_step=1):
    # from the itertools documentation
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    if isinstance(keep_silence, bool):
        keep_silence = len(audio_segment) if keep_silence else 0

    output_ranges = [
        [ start - keep_silence, end + keep_silence ]
        for (start,end)
            in detect_nonsilent(audio_segment, min_silence_len, silence_thresh, seek_step)
    ]
    print(output_ranges)
    output_ranges[0][0]=0;
    output_ranges[0][0]=0;
    output_ranges[len(output_ranges)-1][1]=duration
    print("output range:"+str(len(output_ranges)))
    for i in range(1,len(output_ranges)):
        t=(output_ranges[i-1][1]+output_ranges[i][0])/2
        output_ranges[i][0]=t
        output_ranges[i-1][1]=t
    print("after")
    print(output_ranges)
    for range_i, range_ii in pairwise(output_ranges):
        last_end = range_i[1]
        next_start = range_ii[0]
        if next_start < last_end:
            range_i[1] = (last_end+next_start)//2
            range_ii[0] = range_i[1]

    return [
        audio_segment[ max(start,0) : min(end,len(audio_segment)) ]
        for start,end in output_ranges
    ]

def split_audio_on_silence(audio_file, output_folder, min_silence_len=1000, silence_thresh=-29):
    try:
        audio = AudioSegment.from_file(audio_file)
        duration = len(audio)
        segments = split_on_silence(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh,duration=duration
        )
        return segments
    except Exception as e:
        print(f"Error: {e}")
        return []

def split_and_save_all_audio(input_folder, output_folder, min_silence_len=200, silence_thresh=-29):
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
                    # print(f" {i + 1}  exported to {output_file}")
            else:
                print(f"No segments found in {filename}.")

if __name__ == "__main__":
    input_folder_path = "input"
    output_folder_path = "output"

    split_and_save_all_audio(input_folder_path, output_folder_path)
    # transcriptions = transcribe_all_audio_files("output/data") 
    # for filename, transcription in transcriptions.items():
    #      print(f"Transcription for {filename}: {transcription}")
