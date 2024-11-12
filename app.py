import os
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from music21 import note, chord, stream, instrument
from flask import Flask, render_template, request, send_file
from midi2audio import FluidSynth
import subprocess
from datetime import datetime
from pydub import AudioSegment  # Import pydub

app = Flask(__name__)
app.config['AUDIO_FOLDER'] = 'static/audio/'

# Initialize FluidSynth with the sound font
soundfont_path = 'Z:/MusicGenProject/FluidR3_GM.sf2'
fs = FluidSynth(soundfont_path)


def get_input_sequences(notes, pitchnames, n_vocab):
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    sequence_length = 100
    network_input = []

    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])

    return network_input


def generate_notes(model, network_input, pitchnames, n_vocab, num_notes):
    start = np.random.randint(0, len(network_input) - 1)
    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
    pattern = network_input[start]
    prediction_output = []

    print('Generating notes...')

    for note_index in range(num_notes):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)
        index = np.argmax(prediction)
        result = int_to_note[index]
        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]

    print('Notes Generated...')
    return prediction_output


def create_midi(prediction_output, filename):
    offset = 0
    output_notes = []

    for pattern in prediction_output:
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp=filename)
    return filename


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    duration = int(request.form['duration'])  # Get duration from user
    offset_time = 0.5  # Duration of each note in seconds

    # Calculate the exact number of notes to fit the requested duration
    num_notes = int(duration / offset_time)

    with open('data/notes', 'rb') as filepath:
        notes = pickle.load(filepath)

    pitchnames = sorted(set(item for item in notes))
    n_vocab = len(set(notes))

    network_input = get_input_sequences(notes, pitchnames, n_vocab)

    model = load_model('weights.best.music3.keras')
    print('Model Loaded')

    prediction_output = generate_notes(model, network_input, pitchnames, n_vocab, num_notes)

    # Generate unique filenames with timestamps
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    midi_file = os.path.join(app.config['AUDIO_FOLDER'], f'gen_output_{timestamp}.mid')
    wav_file = os.path.join(app.config['AUDIO_FOLDER'], f'gen_output_{timestamp}.wav')
    mp3_file = os.path.join(app.config['AUDIO_FOLDER'], f'gen_output_{timestamp}.mp3')

    # Generate MIDI and convert to WAV
    create_midi(prediction_output, midi_file)
    fs.midi_to_audio(midi_file, wav_file)

    # Convert WAV to MP3 using FFmpeg
    try:
        subprocess.run(['C:/ffmpeg/bin/ffmpeg.exe', '-i', wav_file, mp3_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting to mp3: {e}")

    # Remove the temporary MIDI and WAV files
    os.remove(midi_file)
    os.remove(wav_file)

    # Pass the MP3 file to the template
    return render_template('index.html', audio_file=mp3_file)


if __name__ == '__main__':
    if not os.path.exists(app.config['AUDIO_FOLDER']):
        os.makedirs(app.config['AUDIO_FOLDER'])
    app.run(debug=True)
