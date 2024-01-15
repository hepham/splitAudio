import os
import speech_recognition as sr
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
def remove_accents_and_uppercase(text):
    text_without_accents = text.replace(',','')
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

if __name__ == "__main__":
    input_folder_path = "output/data"
    text="Dòng sông không chảy thẳng đuột, mà uốn lượn như một con trăn khổng lồ bò từ trên núi xuống. Mặt sông phẳng như tấm gương, đôi chỗ điểm xuyết thêm mấy chùm lục bình có bông hoa tim tím. Nhìn từ xa, mặt sông như đang đứng im, không chảy nữa. Nhưng khi đến gần, ta có thể thấy rõ từng đường chuyển của nước. Dưới lòng sông là một thế giới sôi động và náo nhiệt, khác hẳn phía mặt nước. Ở lớp bùn lầy là rong là cỏ, rồi cua, trai, ốc, hến, lươn. Trong nước thì đủ các đàn cá từ lớn tới bé bơi tới bơi lui."
    sentences=remove_accents_and_uppercase(text).split('.')
    transcriptions = transcribe_all_audio_files(input_folder_path)
    t=0
    check=True
    for filename, transcription in transcriptions.items():
        print(f"Transcription for {filename}: {transcription}")
    #     sub1=transcription.lstrip()[:3]
    #     sub2=sentences[t].lstrip()[:3]
    #     print(sub1)
    #     print(sub2)
    #     if sub1!=sub2: 
    #         print(f"Transcription for {filename}: {transcription}")
    #         print(sentences[t])
    #         check=False
    #         print("error")
            
    #     t+=1
    # if(check):
    #     print("đúng")