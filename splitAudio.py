import pygame
from pydub import AudioSegment

def split_audio(input_file, output_prefix, start_time, end_time):
    audio = AudioSegment.from_file(input_file)
    segment = audio[start_time:end_time]
    output_file = f"{output_prefix}_{start_time}_{end_time}.wav"
    segment.export(output_file, format="wav")
    print(f"Segment exported to {output_file}")
def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    duration_in_seconds = len(audio) 
    return duration_in_seconds
def main():
    input_audio_file = "audio.wav"  # Thay đổi đường dẫn đến file âm thanh của bạn
    output_prefix = "segment"
    
    pygame.init()
    pygame.display.set_mode((640, 640))
    pygame.mixer.init()

    pygame.mixer.music.load(input_audio_file)

    clock = pygame.time.Clock()
    running = True
    playing = False
    start_time = 0
    audioLength=get_audio_duration(input_audio_file)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("vao")
                    if not playing:
                        print("Audio started playing.")
                        pygame.mixer.music.play()
                        playing = True
                    else:
                        end_time = pygame.time.get_ticks()
                        if(end_time>audioLength):end_time=audioLength
                        split_audio(input_audio_file, output_prefix, start_time, end_time)
                        start_time=end_time

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
