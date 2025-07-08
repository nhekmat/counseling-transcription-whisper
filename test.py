# Video https://youtube.com/shorts/MNUdPGIjMPw
# Python 3.10
# pip install openai-whisper
# pip install git+https://github.com/openai/whisper.git 
# install ffmpeg
# brew install ffmpeg

import sys #idek why sys is darkened
import os
import ssl
import sys
# Bypass SSL verification -idek what this does either
ssl._create_default_https_context = ssl._create_unverified_context

import subprocess
import whisper

model = whisper.load_model("base") #small error is 0.17, base is 0.2, tiny is 0.23 
name = input('Input filename without filetype (case sensitive): ')
filetype = input('enter your filetype in (no dots) format: ')
directory = '/Users/michaelhekmat/Documents/coursera/whipserproject/' #sample output but maybe u can have an option to change it in future
video_in = os.path.join(directory+name+'.'+filetype)  # Specify the correct path to your video

if not os.path.exists(video_in):
    print(f'ERROR!  {video_in} does not exist. Try again :(')
    quit()

#audio is stored within whisper folder + idek if its necessary to keep?
# audio_out = input('please insert your audio title') <- basically idek if this is necessary bc idek where audio files are stored

audio_out = 'audio.mp3'  # Specify the correct path for audio output 

#this is original output transcription
# transcription_out = '/Users/michaelhekmat/Documents/coursera/whipserproject/transcript.txt'  # Output file for the transcription
transcript_title = input('please insert your preferred transcription title name: ')
transcription_file = input('please enter file type: ')
transcription_out = directory+transcript_title+'.'+transcription_file

# Convert video to audio using ffmpeg
subprocess.run(["ffmpeg", "-i", video_in, "-vn", "-c:a", "libmp3lame", "-b:a", "192k", audio_out])

# here is block where u can test above block in case u dont wna make 2
# basically see input if
#   A-> does user want to convert from video->audio
#       if YES -> run video->audio cmd and follow audio -> txt
#       if NO->
# try:
#     test = input('do you want to convert from video->audio')
#     if test == 'n':
#         result = model.transcribe(audio_out)
#     if test == 'y':
#         subprocess.run(["ffmpeg", "-i", video_in, "-vn", "-c:a", "libmp3lame", "-b:a", "192k", audio_out])
#         result = model.transcribe(audio_out)
# except:
#     print('error try again')

# Transcribe the audio
result = model.transcribe(audio_out)
# Printing transcribed text so u see it in console
print(result["text"])

# below are 2 options
#   1. you export as a TXT
#   2. you export as a tsv
#   3. be aware that conversion to either format is intensive. Expect battery to drop ~9 percent when unplugged for a 45 minute video

# 1. Exporting as txt function <- idek how this works
# below for getting .txt file output
# with open(transcription_out, 'w') as f:
#     f.write(result["text"])

# #~~~~~~~~BELOW IS JUST FOR TSV IF U DONT WANT THEN IGNORE~~~~~
# 2 Exporting as a .tsv file with timeframes
with open(transcription_out, 'w') as f:
   # Write the header for the .tsv file
    f.write("start_time\tend_time\ttranscription\n")
    
#     # Loop through each segment and write its start time, end time, and text
    for segment in result['segments']:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text'].replace("\n", " ")  # Clean up the text if needed
        
        # Write the segment in TSV format (tab-separated)
        f.write(f"{start_time}\t{end_time}\t{text}\n")

#keep bc its convenient
print(f"Transcription with timestamps saved to {transcription_out}")
