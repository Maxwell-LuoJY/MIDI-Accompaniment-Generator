Make sure you have installed the libraries in requirements.txt

Introduction:
Our project aims to provide an easy-to-use MIDI music production tool for user.
You will be able to input notes via entering key parameters to generate their own melodies.
The program will analyze the your melodies and generate appropriate accompaniment automatically.
The generated music will be stored in MIDI format for convenient replay.
You can use console mode, console mode with music score or graphical mode.

To use console mode:
1. Start by entering 'python basic.py' in your terminal
2. Follow the instructions shown on the terminal.

To use console mode with music score:
1. Start by entering 'python basic.py your_music_score.txt'. For example 'python basic.py two_tigers_major.txt'.

To generate your own music score:
Always include only one parameter in a line.
Follow the following steps.
1. Enter BPM. e.g. 60
2. Enter base note MIDI pitch. e.g. 60 for centre C
3. Enter tonality index. 1 for major tone, 2 for minor tone.
Then, repeat entering notes by
4. Enter the pitch number from 0 to 7, 0 is for rest note.
5. Enter the length of the note, quater note is set as 1.
6. Enter how many octave you want to differ, 0 as default, positive integers for going up, negative integers for going down.
7. Enter the intensity index in range [0,2], 1 for default loudness.
8. Enter 'y' for adding another note.
After finish entering notes
9. Enter 'n' for finish notes input.
10. Enter randomness index for chords, an integer in range [1,4], 1 for lowest randomness.
You can check the two music score samples two_tigers_major.txt and two_tigers_minor.txt for your reference.

GUI mode usage instructions:

Start by running 'python interface.py' in your terminal.
Note: All values that need to be input should be pressed with Enter key.  You can check your computer's terminal to confirm whether you entered it correctly.

1. Choose the tonality of your melody in the upper left corner (Minor or Major)
2. Enter the BPM value
3. Enter your music name
4. Use your keyboard to type your note (the corresponding pitch of the keyboard is shown in the interface, the top is the pitch and the bottom is the keys.)
5. Input the length of the note and select your octave.
6. Click Add button to record the information on this note.
7. Repeat steps 4 to 6 until all notes have been entered, and then click End button.
8. Select the Randomization of your melody.
9. Choose whether you want to add drum, chords, or bass into the melody tracks.
10. Click Play button, user can hear your designed melody.
You can click Sample minor or Sample major button to hear our sample music with minor or major tonality for your reference.