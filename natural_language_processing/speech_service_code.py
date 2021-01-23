### Create a resource

cog_key = 'YOUR_COG_KEY'
cog_endpoint = 'YOUR_COG_ENDPOINT'
cog_region = 'YOUR_COG_REGION'

print('Ready to use cognitive services in {} using key {}'.format(cog_region, cog_key))

#! pip install azure.cognitiveservices.speech


### Speech recognition

import os
import IPython
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig

# Get spoken command from audio file
file_name = 'light-on.wav'
audio_file = os.path.join('data', 'speech', file_name)

# Configure speech recognizer
speech_config = SpeechConfig(cog_key, cog_region)
audio_config = AudioConfig(filename=audio_file) # Use file instead of default (microphone)
speech_recognizer = SpeechRecognizer(speech_config, audio_config)

# Use a one-time, synchronous call to transcribe the speech
speech = speech_recognizer.recognize_once()

# Play audio and show transcribed text
IPython.display.display(IPython.display.Audio(audio_file, autoplay=True),
                        IPython.display.HTML(speech.text))


### Speech synthesis

import os
import IPython
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig

# Get text to be spoken
response_text = 'Turning the light on.'

# Configure speech synthesis
speech_config = SpeechConfig(cog_key, cog_region)
output_file = os.path.join('data', 'speech', 'response.wav')
audio_output = AudioConfig(filename=output_file) # Use a file instead of default (speakers)
speech_synthesizer = SpeechSynthesizer(speech_config, audio_output)

# Transcribe text into speech
result = speech_synthesizer.speak_text(response_text)

# Play the output audio file
IPython.display.display(IPython.display.Audio(output_file, autoplay=True),
                        IPython.display.Image(data=os.path.join("data", "speech" , response_text.lower() + 'jpg')))
                        

### Doc: 
# 1. speech-to-text: https://docs.microsoft.com/azure/cognitive-services/speech-service/index-speech-to-text
# 2. tex-to-speech: https://docs.microsoft.com/azure/cognitive-services/speech-service/index-text-to-speech
