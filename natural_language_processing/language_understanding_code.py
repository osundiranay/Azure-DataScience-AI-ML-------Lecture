from python_code import luis
import matplotlib.pyplot as plt
from PIL import Image
import os
%matplotlib inline

try:
    # Set up API configuration
    luis_app_id = 'YOUR_LU_APP_ID'
    luis_key = 'YOUR_LU_KEY'
    luis_endpoint = 'YOUR_LU_ENDPOINT'

    # prompt for a command
    command = input('Please enter a command: \n')

    # get the predicted intent and entity (code in python_code.home_auto.py)
    action = luis.get_intent(luis_app_id, luis_key, luis_endpoint, command)

    # display an appropriate image
    img_name = action + '.jpg'
    img = Image.open(os.path.join("data", "luis" ,img_name))
    plt.axis('off')
    plt. imshow(img)
except Exception as ex:
    print(ex)
    
###

cog_key = 'YOUR_COG_KEY'
cog_endpoint = 'YOUR_COG_ENDPOINT'
cog_region = 'YOUR_COG_REGION'

print('Ready to use cognitive services in {} using key {}'.format(cog_region, cog_key))

#!pip install azure.cognitiveservices.speech

from python_code import luis
import os
import IPython
import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig

try:   

    # Get spoken command from audio file
    file_name = 'light-on.wav'
    audio_file = os.path.join('data', 'luis', file_name)

    # Configure speech recognizer
    speech_config = SpeechConfig(cog_key, cog_region)
    audio_config = AudioConfig(filename=audio_file) # Use file instead of default (microphone)
    speech_recognizer = SpeechRecognizer(speech_config, audio_config)

    # Use a one-time, synchronous call to transcribe the speech
    speech = speech_recognizer.recognize_once()

    # Get the predicted intent and entity (code in python_code.home_auto.py)
    action = luis.get_intent(luis_app_id, luis_key, luis_endpoint, speech.text)

    # Get the appropriate image
    img_name = action + '.jpg'

    # Play audio and display image
    IPython.display.display(IPython.display.Audio(audio_file, autoplay=True),
                            IPython.display.Image(data=os.path.join("data", "luis" ,img_name)))
except Exception as ex:
    print(ex)
    
### Doc: https://docs.microsoft.com/azure/cognitive-services/luis/
