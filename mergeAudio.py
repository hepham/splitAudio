from pydub import AudioSegment
import speech_recognition as sr
import os
import shutil
import sys
import threading
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

def remove_accents_and_uppercase(text):
    text_without_accents = text.replace(',', '')
    text_lower = text_without_accents.lower()
    return text_lower

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

        try:
            transcription = recognizer.recognize_google(audio_data, language="vi-VN")
            return transcription
        except sr.UnknownValueError:
            print(f"Google Speech Recognition could not understand audio in {audio_file}")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def transcribe_all_audio_files(input_folder):
    transcriptions = {}
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            audio_file_path = os.path.join(input_folder, filename)
            transcription = transcribe_audio(audio_file_path)

            if transcription is not None:
                transcriptions[filename] = transcription

    return transcriptions

def merge_audio(file1_path, file2_path, output_path):
    audio1 = AudioSegment.from_file(file1_path)
    audio2 = AudioSegment.from_file(file2_path)
    merged_audio = audio1 + audio2
    merged_audio.export(output_path, format="wav")

def merge_audio_match_sentence(input_folder, sentences,OUTPUT_DATA_FOLDER,OUTPUT_MERGE_FOLDER,OUTPUT_AUDIO_CUT_FOLDER):
    files = os.listdir(input_folder)
    wav_files = [file for file in files if file.endswith(".wav")]
    n = len(wav_files)
    i = 1
    check = True
    k = 0
    while i < n :
        if check:
            source_path = os.path.join(OUTPUT_DATA_FOLDER, f"{i}.wav")
            destination_path = os.path.join(OUTPUT_MERGE_FOLDER, f"merge{i}.wav")
            shutil.copy2(source_path, destination_path)
            transcription = transcribe_audio(destination_path)
            if transcription == sentences[k]:
                k += 1
                shutil.copy(destination_path, OUTPUT_AUDIO_CUT_FOLDER)
                i += 1
                continue
            else:
                check = False
        else:
            file1_path = os.path.join(OUTPUT_MERGE_FOLDER, f"merge{i}.wav")
            file2_path = os.path.join(OUTPUT_DATA_FOLDER, f"{i + 1}.wav")
            output_path = os.path.join(OUTPUT_MERGE_FOLDER, f"merge{i + 1}.wav")
            merge_audio(file1_path, file2_path, output_path)
            transcription = transcribe_audio(output_path)
            transcription = remove_accents_and_uppercase(transcription)
            print(transcription)
            if transcription == sentences[k]:
                k += 1
                shutil.copy(output_path, OUTPUT_AUDIO_CUT_FOLDER)
                print("Cut successful:"+transcription)
                i += 1
                check = True
            i += 1

def get_sentences(file_path):
    file_content = ""
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return file_content

def split_and_trim(sentence):
    substrings = sentence.split('.')
    trimmed_substrings = [remove_accents_and_uppercase(substring.strip()) for substring in substrings]
    return trimmed_substrings

def sort_wav_files(folder_path):
    wav_files = [file for file in os.listdir(folder_path) if file.endswith(".wav")]
    def extract_number(filename):
        return int(''.join(filter(str.isdigit, filename)))
    sorted_wav_files = sorted(wav_files, key=extract_number)
    for i, old_name in enumerate(sorted_wav_files, start=1):
        extension = os.path.splitext(old_name)[1]
        new_name = f"{i}{extension}"
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)

    return sorted_wav_files
def remove_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents successfully removed.")
    except Exception as e:
        print(f"Failed to remove folder '{folder_path}'")

def handle(OUTPUT_DATA_FOLDER):
    file_path = OUTPUT_DATA_FOLDER +"/data.txt"
    # Get sentences from the file
    text = get_sentences(file_path)
    sentences = split_and_trim(text)
    foldername=OUTPUT_DATA_FOLDER.split("/")[1]
    OUTPUT_MERGE_FOLDER = f"merge/{foldername}"
    OUTPUT_AUDIO_CUT_FOLDER = f"audioCut/{foldername}"
    remove_folder(OUTPUT_AUDIO_CUT_FOLDER)
    os.makedirs(OUTPUT_MERGE_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_AUDIO_CUT_FOLDER, exist_ok=True)
    # Merge audio based on sentences
    merge_audio_match_sentence(OUTPUT_DATA_FOLDER, sentences,OUTPUT_DATA_FOLDER,OUTPUT_MERGE_FOLDER,OUTPUT_AUDIO_CUT_FOLDER)

    # Sort and rename WAV files
    sort_wav_files(OUTPUT_AUDIO_CUT_FOLDER)
    remove_folder(OUTPUT_MERGE_FOLDER)

if __name__ == "__main__":
    # handle("output/data")
    directory="output"
    items = os.listdir(directory)
    # Filter out only the folders
    folders = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    threads = [threading.Thread(target=handle, args=(directory+"/"+folder,)) for folder in folders]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
