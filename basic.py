from mido import Message, MidiFile, MidiTrack, bpm2tempo, MetaMessage
import pygame, random, math, sys


class NotesPlay:
    '''A class to add notes and accompaniments to MIDI track'''
    total_length = 0
    def __init__(self, track, bpm, base, total_len=0, notes_list=[], tonality=1, velocity=1.0):
        self.bpm = bpm
        self.track = track # track in MIDI file
        self.tempo = bpm2tempo(self.bpm) # change bpm to tempo
        self.base = base # base note, center C as default
        self.velocity = round(64*velocity) # loudness
        self.total_len = total_len
        self.notes_list = notes_list
        self.tonality = tonality
        self.meta_time = 480 # time for 1 beat
        self.track.append(MetaMessage('set_tempo', tempo=self.tempo, time=0)) # set tempo
        self.track.append(MetaMessage('time_signature', numerator=4, denominator=4)) # set time signature，numerator=4, denominator=4 is for 4/4 time signature
        self.drum_dict = { # use to check the drums，important instruments are marked as **
            'acoustic_bass': 35,  # 大鼓
            'bass1': 36,  # 低音鼓 **
            'side_stick': 37,  # 边击
            'acoustic_snare': 38,  # 小鼓(松) **
            'hand_clap': 39,  # 拍手
            'electric_snare': 40,  # 小鼓(紧)
            'low_floor_tom': 41,  # 通鼓(最低) **
            'closed_hi-hat': 42,  # 立镲(闭) **
            'high_floor_tom': 43,  # 通鼓(低) **
            'pedal_hi-hat': 44,  # 踩镲
            'low_tom': 45,  # 通鼓(中低) **
            'open_hi-hat': 46,  # 立镲(开) **
            'low-mid_tom': 47,  # 通鼓(中) **
            'hi-mid_tom': 48,  # 通鼓(中高) **
            'crash_cymbal1': 49,  # 低砸音镲 **
            'high_tom': 50,  # 通鼓(高) **
            'ride_cymbal1': 51,  # 厚吊镲(低) **
            'chinese_cymbal': 52,  # 锣
            'ride_bell': 53,  # 厚吊镲(中)
            'tambourine': 54,  # 铃鼓
            'splash_cymbal': 55,  # 小吊镲
            'cowbell': 56,  # 牛铃
            'crash_cymbal2': 57,  # 薄吊镲(高) 高砸音镲
            'vibraslap': 58,  # 振音梆盒
            'ride_cymbal2': 59,  # 厚吊镲(高)
            'hi_bongo': 60,  # 邦戈鼓(高)
            'low_bongo': 61,  # 邦戈鼓(低)
            'mute_hi_bongo': 62,  # 康加鼓(高闭)
            'open_hi_bongo': 63,  # 康加鼓(高开)
            'low_conga': 64,  # 康加鼓(低)
            'high_timbale': 65,  # 边鼓(高)
            'low_timbale': 66,  # 边鼓(低)
            'high_agogo': 67,  # 拉丁打铃(高)
            'low_agogo': 68,  # 拉丁打铃(低)
            'cabasa': 69,  # 喀吧萨
            'maracas': 70,  # 沙锤
            'short_whistle': 71,  # 哨子(短)
            'long_whistle': 72,  # 哨子(长)
            'short_guiro': 73,  # 刮板(短)
            'long_guiro': 74,  # 刮板(长)
            'claves': 75,  # 响棒
            'hi_wood_block': 76,  # 梆盒(高)
            'low_wood_block': 77,  # 梆盒(低)
            'mute_cuica': 78,  # 拉鼓(闭)
            'open_cuica': 79,  # 拉鼓(开)
            'mute_triangle': 80,  # 三角铁(闭)
            'open_triangle': 81  # 三角铁(开)
        }

    def chord_lib(self, chord_type, chord_name): 
        '''Input the name of the chord type (chord_type) and the root note of the chord (chord_name) to get a list of MIDI pitches for the chord.
            !!! Note that both chord_type and chord_name are of type str !!!'''
        base = self.base
        if chord_type == 'major':
            if chord_name == 'C':
                chord =[base, base+4, base+7]
            elif chord_name == 'C#' or chord_name == 'Db':
                chord =[base+1, base+5, base+8]
            elif chord_name == 'D':
                chord =[base+2,base+6, base+9]
            elif chord_name == 'D#' or chord_name=='Eb':
                chord =[base+3, base+7, base+10]
            elif chord_name == 'E':
                chord =[base+4,base+8, base+11]
            elif chord_name == 'F':
                chord =[base+5, base+9, base+12]
            elif chord_name == 'F#' or chord_name == 'Gb':
                chord =[base+6, base+10, base+13]
            elif chord_name == 'G':
                chord = [base+7, base+11, base+14]
            elif chord_name == 'G#' or chord_name == 'Ab':
                chord =[base+8, base+12, base+15]
            elif chord_name == 'A':
                chord =[base+9, base+13, base+16]
            elif chord_name == 'A#':
                chord =[base+10, base+14, base+17]
            elif chord_name == 'B':
                chord =[base+11,base+15,base+18]

        if chord_type == 'minor':
            if chord_name == 'C':
                chord =[base, base+3, base+7]
            elif chord_name == 'C#' or chord_name == 'Db':
                chord =[base+1, base+4, base+8]
            elif chord_name == 'D':
                chord =[base+2,base+5, base+9]
            elif chord_name == 'D#' or chord_name=='Eb':
                chord =[base+3, base+6, base+10]
            elif chord_name == 'E':
                chord =[base+4,base+7, base+11]
            elif chord_name == 'F':
                chord =[base+5, base+8, base+12]
            elif chord_name == 'F#' or chord_name == 'Gb':
                chord =[base+6, base+9, base+13]
            elif chord_name == 'G':
                chord = [base+7, base+10, base+14]
            elif chord_name == 'G#' or chord_name == 'Ab':
                chord =[base+8, base+11, base+15]
            elif chord_name == 'A':
                chord =[base+9, base+12, base+16]
            elif chord_name == 'A#':
                chord =[base+10, base+13, base+17]
            elif chord_name == 'B':
                chord =[base+11,base+14,base+18]
        return chord
    
    def select_tonality(self):
        '''Used to get user input, determine which scale it is, and return a list of distances between adjacent notes in that scale.'''
        while(True):
            tmp = int(input('Please select the tonality of music: 1. Major 2. Minor.'))
            if tmp==1 or tmp==2:
                break
            else:
                print('Invalid input style, try again.')
        return tmp

    def play_note(self, note, length, base_num=0, delay=0, velocity=1.0, music_tonality=1, channel=0, pause_length=0):
        '''Used for the following melody function. Inputs:
            note: range from 1 to 7, corresponding to the scale starting from the tonic.
            Note length (length): if a measure has 4 beats, the range is from 1 to 4, where 1 represents one beat.
            Base number: used to switch the octave, negative values represent lower octaves, positive values represent higher octaves.
            Delay: used to input rests; fill in the number of beats of rest before the current note.
            Velocity: used to adjust the intensity of the current note, range from 0 to 2.
            Channel: don't touch this parameter...
            Pause length: used to add a rest at the end of the melody.
            All above inputs are of type int!'''
        if music_tonality == 1:
            major_notes = [0, 2, 2, 1, 2, 2, 2, 1] # Used to adjust the musical scale, default is C major (the distances between notes are 2-2-1-2-2-2-1, where 1 represents a half step and 2 represents a whole step. To change to minor, use [0, 2, 1, 2, 2, 1, 2, 2].
        elif music_tonality == 2:
            major_notes = [0, 2, 1, 2, 2, 1, 2, 2]
        base_note = self.base
        note_value = base_note + base_num * 12 + sum(major_notes[0:note]) # calculate MIDI note
        self.track.append(Message('note_on', note=note_value, velocity=round(self.velocity*velocity), time=round(delay*self.meta_time), channel=channel))
        self.track.append(Message('note_off', note=note_value, velocity=round(self.velocity*velocity), time=round(self.meta_time*length), channel=channel))
        if pause_length > 0:
            self.track.append(Message('note_off', note=note_value, velocity=0, time=round(self.meta_time * pause_length), channel=channel))
        
    def sample_play_chords(self, chord_type, chord_name, length, base_num=0, delay=0, channel=0, pause_length=0):
        '''Similar to the above play_note function, note that chord_type and chord_name are of type str.'''
        chords = self.chord_lib(chord_type, chord_name)
        for note in chords:
            self.track.append(Message('note_on', note=note+base_num*12, velocity=round(self.velocity), time=round(delay*self.meta_time), channel=channel))
        for note in chords:
            self.track.append(Message('note_off', note=note+base_num*12, velocity=round(self.velocity), time=round(self.meta_time*length), channel=channel))
        if pause_length > 0:
            self.track.append(Message('note_off', note=note+base_num*12, velocity=0, time=round(self.meta_time * pause_length), channel=channel))
        
    def play_chords(self, chords, length, base_num=0, delay=0, channel=0, pause_length=0):
        '''Similar to the above play_note function.'''
        for note in chords:
            self.track.append(Message('note_on', note=note+base_num*12, velocity=round(self.velocity), time=round(delay*self.meta_time), channel=channel))
        for note in chords:
            self.track.append(Message('note_off', note=note+base_num*12, velocity=round(self.velocity), time=round(self.meta_time*length), channel=channel))
        if pause_length > 0:
            self.track.append(Message('note_off', note=note+base_num*12, velocity=0, time=round(self.meta_time * pause_length), channel=channel))

    def sample_melody(self):
        '''Used to generate a melody by repeatedly calling the play_note function to create notes.
            Example: Two Tigers'''
        for i in range(2):
            self.play_note(1, 1) # The first parameter is the pitch, and the second parameter is the length.
            self.play_note(2, 1)
            self.play_note(3, 1)
            self.play_note(1, 1)
        for i in range(2):
            self.play_note(3, 1)
            self.play_note(4, 1)
            self.play_note(5, 2)
        for i in range(2):
            self.play_note(5, 0.5)
            self.play_note(6, 0.5)
            self.play_note(5, 0.5)
            self.play_note(4, 0.5)
            self.play_note(3, 1)
            self.play_note(1, 1)
        for i in range(2):
            self.play_note(2, 1)
            self.play_note(5, 1, base_num=-1)
            self.play_note(1, 2)
    
    def get_melody(self):
        '''Used for user input of note parameters, with four inputs: pitch, length, octave (high/low), and velocity, stored in a sublist.
            Returns a list of lists containing all the note parameters.'''
        notes_list = []
        len = 0
        music_tonality = self.select_tonality()
        while(True):
            notes_sublist = []
            
            while(True):
                note = int(input('Please enter a note (from 0 to 7, 0 for rest note):'))
                if 0<=note<=7:
                    notes_sublist.append(note)
                    break
                else:
                    print('Invalid note, please enter again!')
            
            while(True):
                length = float(input('Please enter the length of this note:'))
                if length>0:
                    notes_sublist.append(length)
                    len+=length
                    break
                else:
                    print('Invalid length (<0), please enter again!')
            
            base_num = int(input('How many octave do you want to go up (0 for no change):'))
            notes_sublist.append(base_num)

            while(True):
                velocity = int(input('Please enter the strength of this note (from 0 to 2, 0 for lowest, 2 for highest, 1 as default):'))
                if 0<=velocity<=2:
                    notes_sublist.append(velocity)
                    break
                else:
                    print('Invalid strength, please enter again!')
            notes_list.append(notes_sublist)
            tmp = input('Do you want to input another note? [y/n]')
            if tmp == 'y':
                continue
            else:
                self.total_length = len
                break
        return notes_list, music_tonality
    
    def generate_melody(self):
        '''Retrieve the list of notes returned by get_melody(), iterate through all the notes in the list, add them to the track, and return the list of notes.'''
        notes_list, music_tonality = self.get_melody()
        is_prev_rest = False
        delay = 0
        for notes in notes_list:
            note = notes[0]
            length = notes[1]
            base_num = notes[2]
            velocity = notes[3]
            if note == 0:
                is_prev_rest = True
                delay = length
                continue
            elif is_prev_rest:
                self.play_note(note=note, length=length, base_num=base_num, delay=delay, velocity=velocity, music_tonality=music_tonality)
                is_prev_rest = False
            else:
                self.play_note(note=note, length=length, base_num=base_num, velocity=velocity, music_tonality=music_tonality)
        return notes_list, self.total_length, music_tonality
    
    def generate_chords(self):
        notes_list = self.notes_list #notes is in[[note, length, base_num, velocity]]
        total_length = self.total_len/4
        num_of_chords = math.ceil(total_length)//4
        print(f'num_of_chord:{num_of_chords}')
        tonality = self.tonality
        if tonality == 1:
            major_notes = [0, 2, 2, 1, 2, 2, 2, 1]
        elif tonality == 2:
            major_notes = [0, 2, 1, 2, 2, 1, 2, 2]
        while(True):
            randomness = int(input('Please select randomness of the generated chords (from 1 to 4, 4 for most random): '))
            if 1<=randomness<=4:
                break
        note = notes_list[0][0]
        base_num = notes_list[0][2]
        base_note = self.base
        note_value = base_note + base_num * 12 + sum(major_notes[0:note])
        if tonality==1:
            chords = [note_value, note_value+4, note_value+7]
        elif tonality==2:
            chords = [note_value, note_value+3, note_value+7]
        tmp = random.randint(1,7)
        note1 = note_value + sum(major_notes[0:tmp])
        if tonality==1:
            chords1 = [note1-4, note1, note1+3]
        elif tonality==2:
            chords1 = [note1-3, note1, note1+4]
        if randomness==1:
            for i in range(num_of_chords):
                for j in range(4):
                    self.play_chords(chords=chords, length=4/3, base_num=-1)
        elif randomness==2:
            for i in range(num_of_chords):
                self.play_chords(chords=chords, length=4/3, base_num=-1)
                self.play_chords(chords=chords, length=4/3, base_num=-1)
                self.play_chords(chords=chords1, length=4/3, base_num=-1)
                self.play_chords(chords=chords, length=4/3, base_num=-1)
        elif randomness==3:
            for i in range(num_of_chords):
                self.play_chords(chords=chords, length=4/3, base_num=-1)
                self.play_chords(chords=chords1, length=4/3, base_num=-1)
                self.play_chords(chords=chords1, length=4/3, base_num=-1)
                self.play_chords(chords=chords, length=4/3, base_num=-1)
        elif randomness==4:
            if tonality==1:
                chords2 = [note1-2, note1+2, note1+5]
            elif tonality==2:
                chords2 = [note1-1, note1+2, note1+6]
            for i in range(num_of_chords):
                self.play_chords(chords=chords, length=4/3, base_num=-1)
                self.play_chords(chords=chords1, length=4/3, base_num=-1)
                self.play_chords(chords=chords2, length=4/3, base_num=-1)
                self.play_chords(chords=chords, length=4/3, base_num=-1)

    def sample_chords(self):
        '''Repeatedly call the play_chord function to generate chords.
            Example: Chords for "Two Tigers," using chords based on root notes 1-1-4-1, with one chord per measure.'''
        for i in range(2):
            self.sample_play_chords('major', 'C', 4/3, base_num=-1) # Note! Although it's unclear why, the third parameter (note length) should be written as beats / number of notes in the chord
            self.sample_play_chords('major', 'C', 4/3, base_num=-1) # (because the default is one chord per measure (4 beats), and each chord has three notes, so it is written as 4/3).
            self.sample_play_chords('major', 'F', 4/3, base_num=-1) # base_num = -1 represents that the chord is lowered by one octave compared to the tonic.
            self.sample_play_chords('major', 'C', 4/3, base_num=-1)
    
    def add_bass(self, note, length, base_num=-2, delay=0, channel=2):
        self.track.append(Message('note_on', note=note+base_num*12, velocity=round(self.velocity), time=round(delay*self.meta_time), channel=channel))
        self.track.append(Message('note_off', note=note+base_num*12, velocity=round(self.velocity), time=round(self.meta_time*length), channel=channel))

    def generate_bass(self):
        notes_list = self.notes_list #notes is in[[note, length, base_num, velocity]]
        total_length = self.total_len/4
        num_of_chords = math.ceil(total_length)
        tonality = self.tonality
        if tonality == 1:
            major_notes = [0, 2, 2, 1, 2, 2, 2, 1]
        elif tonality == 2:
            major_notes = [0, 2, 1, 2, 2, 1, 2, 2]
        note = notes_list[0][0]
        base_num = notes_list[0][2]
        base_note = self.base
        note_value = base_note + base_num * 12 + sum(major_notes[0:note])
        for i in range(num_of_chords):
            self.add_bass(note=note_value, length=0.25)
            self.add_bass(note=note_value+2, length=0.25, delay=0.25)
            self.add_bass(note=note_value+2, length=0.25, delay=0.5)
            self.add_bass(note=note_value, length=1, delay=0.5)
            self.add_bass(note=note_value, length=1)

    def drum(self):
        '''Generate a percussion accompaniment, currently with only one 4/4 beat sample.
            Loops for a number of measures.'''
        print(f'Total length of music:{self.total_len}')
        for i in range(int(self.total_len)//4):
            # The first eighth note: bass drum and crash cymbal hit simultaneously.
            self.track.append(
                Message('note_on', note=self.drum_dict['bass1'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_on', note=self.drum_dict['crash_cymbal1'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['bass1'], velocity=self.velocity, time=round(self.meta_time * 0.5),
                        channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['crash_cymbal1'], velocity=self.velocity, time=0, channel=9))

            # The second eighth note: closed hi-hat.
            self.track.append(
                Message('note_on', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=round(self.meta_time * 0.5),
                        channel=9))

            # The third eighth note: snare drum and closed hi-hat hit simultaneously.
            self.track.append(
                Message('note_on', note=self.drum_dict['acoustic_snare'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_on', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['acoustic_snare'], velocity=self.velocity,
                        time=round(self.meta_time * 0.5), channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=0, channel=9))

            # The fourth eighth note: closed hi-hat.
            self.track.append(
                Message('note_on', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=round(self.meta_time * 0.5),
                        channel=9))

            # The fifth eighth note: bass drum and closed hi-hat hit simultaneously.
            self.track.append(
                Message('note_on', note=self.drum_dict['bass1'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_on', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['bass1'], velocity=self.velocity, time=round(self.meta_time * 0.5),
                        channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=0, channel=9))

            # The sixth eighth note: closed hi-hat.
            self.track.append(
                Message('note_on', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=round(self.meta_time * 0.5),
                        channel=9))

            # The seventh eighth note: snare drum and closed hi-hat hit simultaneously.
            self.track.append(
                Message('note_on', note=self.drum_dict['acoustic_snare'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_on', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['acoustic_snare'], velocity=self.velocity,
                        time=round(self.meta_time * 0.5), channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=0, channel=9))

            # The eighth eighth note: closed hi-hat.
            self.track.append(
                Message('note_on', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=0, channel=9))
            self.track.append(
                Message('note_off', note=self.drum_dict['closed_hi-hat'], velocity=self.velocity, time=round(self.meta_time * 0.5),
                        channel=9))
            

def play_midi(file):
   '''Function in the pygame library used to play MIDI files; input the filename to output audio.'''
   freq = 44100
   bitsize = -16
   channels = 2
   buffer = 1024
   pygame.mixer.init(freq, bitsize, channels, buffer)
   pygame.mixer.music.set_volume(1)
   clock = pygame.time.Clock()
   try:
       pygame.mixer.music.load(file)
   except:
       import traceback
       print(traceback.format_exc())
   pygame.mixer.music.play()
   while pygame.mixer.music.get_busy():
       clock.tick(30)

def write_own():
    music_name = input('Please enter your name of music: ') 
    mid = MidiFile()
    melody_track = MidiTrack()
    chord_track = MidiTrack()
    drum_track = MidiTrack()
    bass_track = MidiTrack()
    mid.tracks.append(melody_track)
    mid.tracks.append(chord_track)
    mid.tracks.append(drum_track)
    mid.tracks.append(bass_track)

    bpm = int(input('Please enter bpm: '))
    base_note = int(input('Please enter base midi note: '))

    notes_list, total_length, tonality = NotesPlay(track=melody_track, bpm=bpm, base=base_note).generate_melody()
    NotesPlay(track=chord_track, bpm=bpm, base=base_note, total_len=total_length, notes_list=notes_list, tonality=tonality, velocity=0.7).generate_chords()
    NotesPlay(track=drum_track, bpm=bpm, base=base_note, total_len=total_length, velocity=0.7).drum()
    NotesPlay(track=bass_track, bpm=bpm, base=base_note, total_len=total_length, notes_list=notes_list, tonality=tonality, velocity=1).generate_bass()

    file_name = music_name + '.mid'
    mid.save(file_name)
    play_midi(file_name)

def use_music_score(filename):
    sys.stdin = open(filename,'r')
    mid = MidiFile()
    melody_track = MidiTrack()
    chord_track = MidiTrack()
    drum_track = MidiTrack()
    bass_track = MidiTrack()
    mid.tracks.append(melody_track)
    mid.tracks.append(chord_track)
    mid.tracks.append(drum_track)
    mid.tracks.append(bass_track)

    bpm = int(input('Please enter bpm: '))
    base_note = int(input('Please enter base midi note: '))

    notes_list, total_length, tonality = NotesPlay(track=melody_track, bpm=bpm, base=base_note).generate_melody() #输入音轨和bpm
    NotesPlay(track=chord_track, bpm=bpm, base=base_note, total_len=total_length, notes_list=notes_list, tonality=tonality, velocity=0.7).generate_chords()
    NotesPlay(track=drum_track, bpm=bpm, base=base_note, total_len=total_length, velocity=0.7).drum()
    NotesPlay(track=bass_track, bpm=bpm, base=base_note, total_len=total_length, notes_list=notes_list, tonality=tonality, velocity=1).generate_bass()

    file_name = filename[:-4] + '.mid'
    mid.save(file_name)
    play_midi(file_name)

if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        write_own()
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        use_music_score(filename)
