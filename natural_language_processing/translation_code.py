### Create a resourse 

cog_key = 'YOUR_COG_KEY'
cog_endpoint = 'YOUR_COG_ENDPOINT'
cog_region = 'YOUR_COG_REGION'

print('Ready to use cognitive services in {} using key {}'.format(cog_region, cog_key))


### Translating text

# Create a function that makes a REST request to the Text Translation service
def translate_text(cog_region, cog_key, text, to_lang='fr', from_lang='en'):
    import requests, uuid, json

    # Create the URL for the Text Translator service REST request
    path = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0'
    params = '&from={}&to={}'.format(from_lang, to_lang)
    constructed_url = path + params

    # Prepare the request headers with Cognitive Services resource key and region
    headers = {
        'Ocp-Apim-Subscription-Key': cog_key,
        'Ocp-Apim-Subscription-Region':cog_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Add the text to be translated to the body
    body = [{
        'text': text
    }]

    # Get the translation
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return response[0]["translations"][0]["text"]


# Test the function
text_to_translate = "Hello"

translation = translate_text(cog_region, cog_key, text_to_translate, to_lang='fr', from_lang='en')
print('{} -> {}'.format(text_to_translate,translation))

text_to_translate = "Hello"

translation = translate_text(cog_region, cog_key, text_to_translate, to_lang='it-IT', from_lang='en-GB')
print('{} -> {}'.format(text_to_translate,translation))

text_to_translate = "Hello"

translation = translate_text(cog_region, cog_key, text_to_translate, to_lang='zh-CN', from_lang='en-US')
print('{} -> {}'.format(text_to_translate,translation))


### Speech translation

#! pip install azure.cognitiveservices.speech

# Create a function to translate audio in one language to text in another
def translate_speech(cog_region, cog_key, audio_file=None, to_lang='fr-FR', from_lang='en-US'):
    from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, ResultReason
    from azure.cognitiveservices.speech.translation import SpeechTranslationConfig, TranslationRecognizer

    # Configure the speech translation service
    translation_config = SpeechTranslationConfig(subscription=cog_key, region=cog_region)
    translation_config.speech_recognition_language = from_lang
    translation_config.add_target_language(to_lang)

    # Configure audio input
    if audio_file is None:
        audio_config = AudioConfig() # Use default input (microphone)
    else:
        audio_config = AudioConfig(filename=audio_file) # Use file input

    # Create a translation recognizer and use it to translate speech input
    recognizer = TranslationRecognizer(translation_config, audio_config)
    result = recognizer.recognize_once()

    # Did we get it?
    translation = ''
    speech_text = ''
    if result.reason == ResultReason.TranslatedSpeech:
        speech_text = result.text
        translation =  result.translations[to_lang]
    elif result.reason == ResultReason.RecognizedSpeech:
        speech_text = result.text
        translation =  'Unable to translate speech'
    else:
        translation = 'Unknown'
        speech_text = 'Unknown'

    # rturn the translation
    return speech_text, translation
    

# Test the function
import os, IPython

file_name = 'english.wav'
file_path = os.path.join('data', 'translation', file_name)
speech, translated_speech = translate_speech(cog_region, cog_key, file_path, to_lang='es', from_lang='en-US')
result = '{} -> {}'.format(speech, translated_speech)

# Play audio and show translated text
IPython.display.display(IPython.display.Audio(file_path, autoplay=True),
                        IPython.display.HTML(result))
                        
import os, IPython

file_name = 'french.wav'
file_path = os.path.join('data', 'translation', file_name)
speech, translated_speech = translate_speech(cog_region, cog_key, file_path, to_lang='en', from_lang='fr-FR')
result = '{} -> {}'.format(speech, translated_speech)

# Play audio and show translated text
IPython.display.display(IPython.display.Audio(file_path, autoplay=True),
                        IPython.display.HTML(result))
                        
### Doc: 
# 1. Translator Text: https://docs.microsoft.com/azure/cognitive-services/translator/
# 2. Speech service: https://docs.microsoft.com/azure/cognitive-services/speech-service/index-speech-translation
