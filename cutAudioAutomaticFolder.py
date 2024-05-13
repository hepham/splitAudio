import itertools
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_nonsilent
import shutil
import pandas as pd
def split_on_silence(listAudio, min_silence_len=1000, silence_thresh=-16, keep_silence=100,
                     seek_step=1):
    """
    Returns list of audio segments from splitting audio_segment on silent sections

    audio_segment - original pydub.AudioSegment() object

    min_silence_len - (in ms) minimum length of a silence to be used for
        a split. default: 1000ms

    silence_thresh - (in dBFS) anything quieter than this will be
        considered silence. default: -16dBFS

    keep_silence - (in ms or True/False) leave some silence at the beginning
        and end of the chunks. Keeps the sound from sounding like it
        is abruptly cut off.
        When the length of the silence is less than the keep_silence duration
        it is split evenly between the preceding and following non-silent
        segments.
        If True is specified, all the silence is kept, if False none is kept.
        default: 100ms

    seek_step - step size for interating over the segment in ms
    """
    audio_segment=listAudio[0]
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

    for range_i, range_ii in pairwise(output_ranges):
        last_end = range_i[1]
        next_start = range_ii[0]
        if next_start < last_end:
            range_i[1] = (last_end+next_start)//2
            range_ii[0] = range_i[1]
    # for start,end in output_ranges:
    #     print(f"timeStamp:{start}-{end}")
    mapAudio={}
    listFolder=["0m","1m","2m","3m","5m"]
    index=0
    for audio_segment in listAudio:
        mapAudio[listFolder[index]]=[]
        for start,end in output_ranges:
            mapAudio[listFolder[index]].append(audio_segment[ max(start,0) : min(end,len(audio_segment)) ])
        index+=1
    return mapAudio

def split_audio_on_silence(list_audio_file_path, output_folder, min_silence_len=3000, silence_thresh=-40):
    try:
        listAudio=[]
        for audio_file in list_audio_file_path:
            audio = AudioSegment.from_file(audio_file)
            listAudio.append(audio)
        segments = split_on_silence(
            listAudio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh,keep_silence=1000
        )
        return segments
    except Exception as e:
        print(f"Error: {e}")
        return []

def split_and_save_all_audio(input_folder, output_folder, min_silence_len=2000, silence_thresh=-40):
    folder_list=[folder for folder in os.listdir(input_folder)if os.path.isdir(os.path.join(input_folder, folder))]
    # for folder in folder_list:
    #     print(folder)
    #     file_folder=os.path.join(input_folder,folder)
    #     for filename in os.listdir(file_folder):
    #         if filename.endswith(".wav"):
    #             audio_file_path = os.path.join(file_folder, filename)
    #             segments = split_audio_on_silence(audio_file_path, output_folder, min_silence_len, silence_thresh)
    #             if segments:
    #                 audio_name = os.path.splitext(filename)[0]
    #                 subfolder = os.path.join(os.path.join(output_folder,os.path.basename(file_folder), audio_name))
    #                 os.makedirs(subfolder, exist_ok=True)
    #                 # shutil.copy(audio_file_path, subfolder)
    #                 for i, segment in enumerate(segments):
    #                     # print(segment)
    #                     output_file = os.path.join(subfolder, f"{i + 1}.wav")
    #                     segment.export(output_file, format="wav")
    #                     print(f" {i + 1}  exported to {output_file}")
    #             else:
    #                 print(f"No segments found in {filename}.")
    listFolderName=["1m","2m","3m","5m"]
    file_folder=os.path.join(input_folder,"0m")
    for filename in os.listdir(file_folder):
        if filename.endswith(".wav"):
            audio_file_path = os.path.join(file_folder, filename)
            # print(audio_file_path)
            list_audio_file_path=[]
            list_audio_file_path.append(audio_file_path)
            for foldername in listFolderName:
                audio_file_path = os.path.join(input_folder,foldername, filename)
                list_audio_file_path.append(audio_file_path)
            segmentMap = split_audio_on_silence(list_audio_file_path, output_folder, min_silence_len, silence_thresh)
            for key,segments in segmentMap.items():
                if segments:
                    audio_name = os.path.splitext(filename)[0]
                    subfolder = os.path.join(os.path.join(output_folder,os.path.basename(key), audio_name))
                    os.makedirs(subfolder, exist_ok=True)
                    # shutil.copy(audio_file_path, subfolder)
                    for i, segment in enumerate(segments):
                        # print(segment)
                        output_file = os.path.join(subfolder, f"{i + 1}.wav")
                        segment.export(output_file, format="wav")
                        # print(f" {i + 1}  exported to {output_file}")
                else:
                    print(f"No segments found in {filename}.")
def removeFailRecord(excelPath):
    data=pd.read_excel(excelPath)
    audioIndex=0
    listAudio=[]
    for index,row in data.iterrows():
        value=str(row["Time"])
        if value!="nan":
            audioIndex+=int (float(value))
            listAudio.append(audioIndex)
        else:
            audioIndex+=1
            listAudio.append(audioIndex)
    return listAudio
        
    
if __name__ == "__main__":
    input_folder_path = "input"
    output_folder_path = "output"

    split_and_save_all_audio(input_folder_path, output_folder_path)
    listAudio=removeFailRecord("data.xlsx")
    print(listAudio)
