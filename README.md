
# Music Generation with Neural Networks

This project demonstrates how to train a neural network model to generate music based on MIDI files and use the trained model to create new music sequences. The application is built using Flask to generate audio files and provide a web interface for users to interact with the model. 

## Project Overview

The goal of this project is to train a Long Short-Term Memory (LSTM) model on MIDI files of piano music to generate new, original sequences based on the patterns in the data. Once the model is trained, users can input the duration of the music they wish to generate, and the system will create a corresponding MIDI file, convert it to WAV, and then convert it to MP3 for easy playback.

### Technologies Used
- **Python**: Programming language used for both training the model and developing the web application.
- **Flask**: Web framework used to create the app and serve the generated music.
- **TensorFlow/Keras**: Deep learning library used to build and train the LSTM model.
- **Music21**: A toolkit for analyzing and working with musical data, used to parse and process MIDI files.
- **FluidSynth**: A software synthesizer for converting MIDI files into audio.
- **pydub**: Used for converting audio files between formats (WAV to MP3).
- **FFmpeg**: Used to handle the conversion of WAV files to MP3.

## Project Structure

```
MusicGenProject/
├── data/                   # Folder for storing datasets
├── myenv/                  # Virtual environment folder (not tracked by Git)
├── static/                 # Static files like CSS and JavaScript
├── templates/              # HTML templates for the web interface
├── app.py                  # Main application script
├── play.py                 # Script to play generated music
├── requirements.txt        # Dependencies
├── README.md               # Project information
└── .gitignore       # Jupyter notebook for training the music generation model
```

## How It Works

### Model Training

1. **Data Preprocessing**: The first step involves processing MIDI files to extract musical notes and chords. These are then encoded into integer representations for use as input/output sequences for the model.
2. **Network Architecture**: The model consists of two LSTM layers, followed by a Dense layer, designed to predict the next note in a sequence based on the previous notes.
3. **Training**: The LSTM model is trained on the prepared sequences. A checkpoint is saved during training to store the best weights for generating music.
4. **Saving the Model**: After training, the model is saved in the file `weights.best.music3.keras`.

### Music Generation (Flask App)

1. **User Input**: Users specify the desired duration of music (in seconds) they wish to generate.
2. **Sequence Generation**: The Flask app loads the trained model and the notes from the `data/notes` file. The input notes are used to generate new sequences based on the model's predictions.
3. **MIDI File Creation**: The generated notes are converted back into MIDI format using `music21`, then stored as a `.mid` file.
4. **Audio Conversion**: The generated MIDI file is converted to audio (WAV) using FluidSynth, and then converted to MP3 using FFmpeg for easier playback.
5. **Downloadable Audio**: The final MP3 file is made available for download from the web interface.

### Web Interface

- **Flask Web App**: The app allows users to generate music sequences by entering the desired duration. The output is an MP3 file that can be played or downloaded.
- **`index.html`**: This HTML template provides the user interface for generating and downloading the music.

## Requirements

To run the project locally, you need the following dependencies:

- Python 3.6+
- Flask
- TensorFlow 2.x
- Keras
- Music21
- pydub
- FluidSynth
- FFmpeg (for audio conversion)


### Additional Requirements

- **FluidSynth**: You need to install the `FluidR3_GM.sf2` soundfont file to convert MIDI to audio. You can download it from the FluidSynth website or other sources.
  - After downloading, place the `FluidR3_GM.sf2` file in the directory where the app can access it (e.g., `./soundfont/`).
  - Ensure that the path to this soundfont file is correctly referenced in the code.

To install FluidSynth and FFmpeg, you may need to download and install them manually based on your operating system.

## How to Run the Application

1. Clone the repository to your local machine:
   ```bash
   git clone <repository_url>
   cd MusicGenProject
   ```

2. Install the required Python packages
  

3. Ensure that you have the **`FluidR3_GM.sf2` soundfont** installed and placed in the correct directory as specified in the code (`soundfont_path`).
4. Run the Flask app:
   ```bash
   python app.py
   ```

5. Open a browser and navigate to `http://127.0.0.1:5000/` to use the app.

6. To train the model (if not already done), run the training script:
   ```bash
   python train_notebook.py
   ```

### Generate Music

- Navigate to the web interface and input the desired duration of the music.
- The app will generate a music file (in MP3 format) based on your input.

### Notes

- This project is limited to generating piano music based on the MIDI files provided.
- Ensure that FFmpeg is correctly installed and accessible for audio conversion from WAV to MP3.


