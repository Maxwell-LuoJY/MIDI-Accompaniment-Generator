import pygame
import sys
import threading
import matplotlib.pyplot as plt
import matplotlib
from gui_components import InputBox, Button, Label, Image, ToggleButton, DropdownMenu, KeyMapper
from basic import NotesPlay, play_midi
from mido import Message, MidiFile, MidiTrack, bpm2tempo, MetaMessage
import mido

CLICK_BAR = False
START_TIME = 0

def midi_to_time_pitch_image(midi_file):
    mid = mido.MidiFile(midi_file)
    notes_by_track = {}  # 存储每个轨道的音符

    for track_index, track in enumerate(mid.tracks):
        current_time = 0
        notes = []

        # 读取 MIDI 文件中的音符
        for msg in track:
            current_time += msg.time  # 更新当前时间
            if msg.type == 'note_on':
                notes.append((current_time, msg.note))  # 记录音符开始

        notes_by_track[track_index] = notes  # 将轨道的音符存储到字典中

    # 创建一个图形
    plt.figure(figsize=(12, 6))

    # 绘制每个轨道的音符
    for track_index, notes in notes_by_track.items():
        times = [note[0] for note in notes]  # 获取时间
        pitches = [note[1] for note in notes]  # 获取音高
        plt.scatter(times, pitches, alpha=0.6, s=10)  # 绘制散点，不加标签

    # 自动调整 X 轴和 Y 轴范围
    all_times = [note[0] for notes in notes_by_track.values() for note in notes]
    all_pitches = [note[1] for notes in notes_by_track.values() for note in notes]

    # 动态设置 x 和 y 轴范围
    plt.xlim(min(all_times), max(all_times))  # 时间范围
    plt.ylim(min(all_pitches) - 1, max(all_pitches) + 1)  # 音高范围

    # 移除所有注释和标签
    plt.axis('off')

    # 保存图像，不显示
    image_file = midi_file[:-4] + "_image.png"
    plt.savefig(image_file, bbox_inches='tight', pad_inches=0)
    return image_file

def get_total_time(midi_file):
    mid = mido.MidiFile(midi_file)
    ticks_per_beat = mid.ticks_per_beat
    tempo = 500000  # 默认tempo
    total_ticks = 0

    for track in mid.tracks:
        current_ticks = 0
        for msg in track:
            current_ticks += msg.time
            if msg.type == 'set_tempo':
                tempo = msg.tempo
            if msg.type == 'note_on':
                total_ticks = max(total_ticks, current_ticks)

    total_seconds = (total_ticks * tempo) / (ticks_per_beat * 1_000_000)
    return total_seconds


def draw_progress_bar(screen, progress, x, y, width, height, color, bg_color):
    pygame.draw.rect(screen, bg_color, (x, y, width, height))
    pygame.draw.rect(screen, color, (x, y, width * progress, height))

def play_music(info, add_drum, add_chord, add_base):

    file_name = info["file_name"][:-4] + ".txt"
    sys.stdin = open(file_name,'r')
    mid = MidiFile()
    melody_track = MidiTrack()
    chord_track = MidiTrack()
    drum_track = MidiTrack()
    bass_track = MidiTrack()
    mid.tracks.append(melody_track)
    notes_list, total_length, tonality = NotesPlay(track=melody_track, bpm=info["bpm"], base=60).generate_melody()
    if info["bpm"] is not None and info["file_name"] is not None:
        if add_drum: 
            mid.tracks.append(drum_track)
            NotesPlay(track=drum_track, bpm=info["bpm"], base=60, total_len=total_length, velocity=0.7).drum()
        if add_chord:
            mid.tracks.append(chord_track)
            NotesPlay(track=chord_track, bpm=info["bpm"], base=60, total_len=total_length, notes_list=notes_list, tonality=tonality, velocity=0.7).generate_chords()
        if add_base:
            mid.tracks.append(bass_track)
            NotesPlay(track=bass_track, bpm=info["bpm"], base=60, total_len=total_length, notes_list=notes_list, tonality=tonality, velocity=1).generate_bass()
        mid.save(info["file_name"])
    elif info["file_name"] is not None:
        print("Please enter the bpm")
    elif info["bpm"] is not None:
        print("Please enter the music name")
    else:
        print("please enter bpm and music name")
        
def write_txt(info):
    file_name = info["file_name"][:-4] + '.txt'
    data = [info["bpm"], 60, info["is_minor"]]
    l = len(info["note"])
    j = 1
    for i in info["note"]:
        data.append(i["note_value"])
        data.append(i["length_note"])
        data.append(i["octave"])
        data.append(1)
        if j < l:
            data.append("y")
        else:
            data.append("n")
        j += 1
    data.append(info["random"])
    with open(file_name, 'w') as file:
        for item in data:
            file.write(f"{item}\n")
    

pygame.init()
pygame.mixer.init()

# set up the size of window
screen_width, screen_height = 1200, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Accompaniment Generator")


# Label
header = Label(screen_width // 2, 30, "Accompaniment Generator", font_size=40, text_color=(0, 0, 0), border_color=(255, 192, 203), border_thickness=10, is_center=1)
text1 = Label(30, 120, "Input your melody!", font_size=30, text_color=(0, 0, 0), border_color=(255, 255, 255))
text2 = Label(30, 410, "Your melody:", font_size=25, text_color=(0, 0, 0), border_color=(255, 255, 255))
text3 = Label(500, 130, "Length of note:", font_size=20, text_color=(0, 0, 0), border_color=(255, 255, 255))
text4 = Label(780, 130, "Quarter note is considered as 1", font_size=15, text_color=(128, 128, 128), border_color=(255, 255, 255))
text5 = Label(30, 610, "BPM", font_size=20, text_color=(0, 0, 0), border_color=(255, 255, 255))
text6 = Label(30, 660, "Drum", font_size=20, text_color=(0, 0, 0), border_color=(255, 255, 255))
text7 = Label(30, 710, "Chords", font_size=20, text_color=(0, 0, 0), border_color=(255, 255, 255))
text8 = Label(400, 560, "Name of music", font_size=20, text_color=(0, 0, 0), border_color=(255, 255, 255))
text9 = Label(30, 30, "Minor", font_size=20, text_color=(0, 0, 0), border_color=(255, 255, 255))
text10 = Label(30, 65, "Major", font_size=20, text_color=(0, 0, 0), border_color=(255, 255, 255))
text11 = Label(500, 220, "Octave:", font_size=20, text_color=(0, 0, 0), border_color=(255, 255, 255))
text12 = Label(30, 760, "Bass:", font_size=20, text_color=(0, 0, 0), border_color=(255, 255, 255))
text13 = Label(400, 630, "Randomness", font_size=20, text_color=(0, 0, 0), border_color=(255, 255, 255))

# InputBox
length_note_input_box = InputBox(650, 130, 100, 30, 20)
bpm_input_box = InputBox(150, 610, 100, 30, 20)
music_name_input_box = InputBox(400, 590, 200, 30, 20)

# Button
def button_action():
    print("Button clicked!")


add_button = Button(500, 300, 'images/add.png', 117, 63, action=button_action)
end_button = Button(650, 300, 'images/end.png', 117, 63, action=write_txt)
delete_button = Button(800, 550, 'images/delete.png', 120, 31, action=button_action)
empty_button = Button(950, 550, 'images/empty.png', 120, 31, action=button_action)
play_button = Button(880, 720, 'images/play.png', 117, 63, action=play_midi)
sample_minor_button = Button(880, 220, 'images/sample_minor.png', 117, 63, action=play_midi)
sample_major_button = Button(880, 320, 'images/sample_major.png', 117, 63, action=play_midi)

drum_toggle_button = ToggleButton(150, 660, "images/toggle_button_on.png", "images/toggle_button_off.png", 50, 30)
chord_toggle_button = ToggleButton(150, 710, "images/toggle_button_on.png", "images/toggle_button_off.png", 50, 30)
base_toggle_button = ToggleButton(150, 760, "images/toggle_button_on.png", "images/toggle_button_off.png", 50, 30)
minor_toggle_button = ToggleButton(100, 30, "images/toggle_button_on.png", "images/toggle_button_off.png", 50, 30)
major_toggle_button = ToggleButton(100, 65, "images/toggle_button_on.png", "images/toggle_button_off.png", 50, 30)

# Image
piano = Image(30, 200, "images/piano.png", 320, 185)

# DropdownMenu
octave_menu = DropdownMenu(650, 220, 150, 30, ["-1", "0", "1"], "Select your octave")
random_menu = DropdownMenu(400, 660, 200, 30, ["1", "2", "3", "4"], "Choose the randomization")

# Key mapper
key_mapper = KeyMapper()

running = True
clock = pygame.time.Clock()
info = {"is_minor": None, "bpm": None, "file_name": None, "random": 1, "note": []}
current_notes = []
note = {"note_value": None, "octave": None, "length_note" : None}
show_midi_graph = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if add_button.is_clicked(event.pos):
                    if note["length_note"] is None:
                        print("Please enter the length of note")
                    elif note["octave"] is None:
                        print("Please choose the octave")
                    elif note["note_value"] is None:
                        print("Please enter note value")
                    else:
                        info["note"].append(note)
                        print(info["note"])
                        note = {"note_value": None, "octave": None, "length_note" : None}

                delete_button.is_clicked(event.pos)
                empty_button.is_clicked(event.pos)

                drum_toggle_button.is_clicked(event.pos)
                chord_toggle_button.is_clicked(event.pos)
                base_toggle_button.is_clicked(event.pos)

                if minor_toggle_button.is_clicked(event.pos):
                    info["is_minor"] = 2
                if major_toggle_button.is_clicked(event.pos):
                    info["is_minor"] = 1
                if play_button.is_clicked(event.pos):
                    play_music(info, drum_toggle_button.is_on, chord_toggle_button.is_on, base_toggle_button.is_on)
                    threading.Thread(target=play_midi, args=(info["file_name"], )).start()
                    CLICK_BAR = True
                    image_file = midi_to_time_pitch_image(info["file_name"])
                    image1 = Image(30, 440, image_file, 1100, 75)
                    START_TIME = pygame.time.get_ticks()

                if end_button.is_clicked(event.pos):
                    if info["is_minor"] is None:
                        print("Please choose tonality")
                    elif info["bpm"] is None:
                        print("Please enter bpm")
                    elif info["file_name"] is None:
                        print("Please enter music name")
                    elif len(info["note"]) == 0:
                        print("Please enter note")
                    else:
                        write_txt(info)

                if sample_minor_button.is_clicked(event.pos):
                    threading.Thread(target=play_midi, args=("sample_minor.mid", )).start()
                    info["file_name"] = "sample_minor.mid"
                    CLICK_BAR = True
                    image_file = midi_to_time_pitch_image(info["file_name"])
                    image1 = Image(30, 440, image_file, 1100, 75)
                    START_TIME = pygame.time.get_ticks()

                if sample_major_button.is_clicked(event.pos):
                    threading.Thread(target=play_midi, args=("sample_major.mid", )).start()
                    info["file_name"] = "sample_minor.mid"
                    CLICK_BAR = True
                    image_file = midi_to_time_pitch_image(info["file_name"])
                    image1 = Image(30, 440, image_file, 1100, 75)
                    START_TIME = pygame.time.get_ticks()

        octave = octave_menu.handle_event(event)
        if octave:
            print("Octave: ", octave)
            note["octave"] = int(octave)
        
        random = random_menu.handle_event(event)
        if random:
            print("Random:", random)
            info["random"] = int(random)

        if not (length_note_input_box.is_focused() or bpm_input_box.is_focused() or music_name_input_box.is_focused()):
            value = key_mapper.get_key_value(event)
            if value is not None:
                print("Value: ", value)
                note["note_value"] = int(value)

        # Input box handling
        length_note = length_note_input_box.handle_event(event)
        bpm = bpm_input_box.handle_event(event)
        music_name = music_name_input_box.handle_event(event)
        if length_note is not None:
            print("Length of note:", length_note)
            note["length_note"] = int(length_note)
        if bpm is not None:
            print("BPM: ", bpm)
            info["bpm"] = int(bpm)
        if music_name is not None:
            print("Music name: ", music_name)
            info["file_name"] = music_name + ".mid"

    # Plot
    screen.fill((255, 255, 255))

    # Input box plot
    length_note_input_box.draw(screen)
    bpm_input_box.draw(screen)
    music_name_input_box.draw(screen)

    # Label plot
    header.draw(screen)
    text1.draw(screen)
    text2.draw(screen)
    text3.draw(screen)
    text4.draw(screen)
    text5.draw(screen)
    text6.draw(screen)
    text7.draw(screen)
    text8.draw(screen)
    text9.draw(screen)
    text10.draw(screen)
    text11.draw(screen)
    text12.draw(screen)
    text13.draw(screen)

    # Button plot
    add_button.draw(screen)
    end_button.draw(screen)
    delete_button.draw(screen)
    empty_button.draw(screen)
    play_button.draw(screen)
    sample_major_button.draw(screen)
    sample_minor_button.draw(screen)
    drum_toggle_button.draw(screen)
    chord_toggle_button.draw(screen)
    minor_toggle_button.draw(screen)
    major_toggle_button.draw(screen)
    base_toggle_button.draw(screen)
    
    # Image plot
    piano.draw(screen)
    octave_menu.draw(screen)
    random_menu.draw(screen)
    if CLICK_BAR:
        image1.draw(screen)

    if CLICK_BAR:
        midi_file = info['file_name']  # 替换为你的 MIDI 文件路径
        total_time = get_total_time(midi_file)
        bar_width = screen_width - 10
        bar_height = 10
        bar_x = 5
        bar_y = 530
        bar_color = (0, 128, 255)
        bar_bg_color = (200, 200, 200)
        elapsed_time = (pygame.time.get_ticks() - START_TIME) / 1000  # 将毫秒转换为秒
        progress = min(elapsed_time / total_time, 1)
        print(progress)
        draw_progress_bar(screen, progress, bar_x, bar_y, bar_width, bar_height, bar_color, bar_bg_color)
        if progress >= 1:
            CLICK_BAR = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
