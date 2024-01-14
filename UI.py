import pygame
import os
from tkinter import Tk, filedialog
from pydub import AudioSegment

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
HOVER_BLUE = (0, 200, 255)

# Initialize Pygame
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Audio Player")

font = pygame.font.Font(None, 36)
selected_folder = ""
audio_files = []
current_audio_index = 0
current_audio = None
cut_folder = "cut_audio"

def draw_button(rect, color, text):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_textbox(rect, text):
    pygame.draw.rect(screen, WHITE, rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(left=rect.left + 10, centery=rect.centery)
    screen.blit(text_surface, text_rect)

def select_folder():
    global selected_folder, audio_files, current_audio_index, current_audio

    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    root.destroy()

    if folder_path:
        selected_folder = folder_path
        audio_files = [f for f in os.listdir(selected_folder) if f.endswith(".wav")]
        current_audio_index = 0
        load_current_audio()

def load_current_audio():
    global current_audio
    if audio_files:
        current_audio_path = os.path.join(selected_folder, audio_files[current_audio_index])
        current_audio = AudioSegment.from_file(current_audio_path)
        print("Loaded:", current_audio_path)

def play_current_audio():
    if current_audio:
        pygame.mixer.music.load(current_audio.export(format="wav", codec="wav"))
        pygame.mixer.music.play()

def cut_audio(start_time, end_time):
    global current_audio, selected_folder

    if current_audio:
        cut_segment = current_audio[start_time:end_time]
        cut_folder_path = os.path.join(selected_folder, cut_folder)
        os.makedirs(cut_folder_path, exist_ok=True)
        output_file = os.path.join(cut_folder_path, f"{audio_files[current_audio_index]}_{start_time}_{end_time}.wav")
        cut_segment.export(output_file, format="wav")
        print(f"Segment exported to {output_file}")

def main():
    pygame.mixer.init()

    clock = pygame.time.Clock()
    running = True
    playing = False
    start_time = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    play_current_audio()
                elif event.key == pygame.K_RIGHT:
                    current_audio_index = (current_audio_index + 1) % len(audio_files)
                    load_current_audio()
                    play_current_audio()
                elif event.key == pygame.K_DOWN:
                    current_audio_index = 0
                    load_current_audio()
                    play_current_audio()
                elif event.key == pygame.K_SPACE:
                    end_time = pygame.time.get_ticks()
                    cut_audio(start_time, end_time)
                    start_time = end_time

        screen.fill(BLUE)

        # Vẽ button
        select_button = pygame.Rect(50, 50, 200, 50)
        if select_button.collidepoint(pygame.mouse.get_pos()):
            draw_button(select_button, HOVER_BLUE, "Select Folder")
        else:
            draw_button(select_button, BLUE, "Select Folder")

        # Vẽ textbox
        textbox_rect = pygame.Rect(50, 120, 400, 30)
        draw_textbox(textbox_rect, selected_folder)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    select_folder()  # Automatically select folder at the beginning
    main()
