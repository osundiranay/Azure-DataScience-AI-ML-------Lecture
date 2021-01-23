### View documents

import os

# Read the reviews in the /data/reviews folder
reviews_folder = os.path.join('data', 'text', 'reviews')

# Create a collection of reviews with id (file name) and text (contents) properties
reviews = []
for file_name in os.listdir(reviews_folder):
    review_text = open(os.path.join(reviews_folder, file_name)).read()
    review = {"id": file_name, "text": review_text}
    reviews.append(review)

for review_num in range(len(reviews)):
    # print the review text
    print('{}\n{}\n'.format(reviews[review_num]['id'], reviews[review_num]['text']))
    

### Create a resource

cog_key = 'YOUR_COG_KEY'
cog_endpoint = 'YOUR_COG_ENDPOINT'

print('Ready to use cognitive services at {} using key {}'.format(cog_endpoint, cog_key))

#! pip install azure-cognitiveservices-language-textanalytics


### Detect language 

import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

# Get a client for your text analytics cognitive service resource
text_analytics_client = TextAnalyticsClient(endpoint=cog_endpoint,
                                            credentials=CognitiveServicesCredentials(cog_key))

# Analyze the reviews you read from the /data/reviews folder earlier
language_analysis = text_analytics_client.detect_language(documents=reviews)

# print detected language details for each review
for review_num in range(len(reviews)):
    # print the review id
    print(reviews[review_num]['id'])

    # Get the language details for this review
    lang = language_analysis.documents[review_num].detected_languages[0]
    print(' - Language: {}\n - Code: {}\n - Score: {}\n'.format(lang.name, lang.iso6391_name, lang.score))

    # Add the detected language code to the collection of reviews (so we can do further analysis)
    reviews[review_num]["language"] = lang.iso6391_name
    

### Extract key phrases

# # Use the client and reviews you created in the previous code cell to get key phrases
key_phrase_analysis = text_analytics_client.key_phrases(documents=reviews)

# print key phrases for each review
for review_num in range(len(reviews)):
    # print the review id
    print(reviews[review_num]['id'])

    # Get the key phrases in this review
    print('\nKey Phrases:')
    key_phrases = key_phrase_analysis.documents[review_num].key_phrases
    # Print each key phrase
    for key_phrase in key_phrases:
        print('\t', key_phrase)
    print('\n')
 
 
### Determine sentiment

# Use the client and reviews you created previously to get sentiment scores
sentiment_analysis = text_analytics_client.sentiment(documents=reviews)

# Print the results for each review
for review_num in range(len(reviews)):

    # Get the sentiment score for this review
    sentiment_score = sentiment_analysis.documents[review_num].score

    # classifiy 'positive' if more than 0.5, 
    if sentiment_score < 0.5:
        sentiment = 'negative'
    else:
        sentiment = 'positive'

    # print file name and sentiment
    print('{} : {} ({})'.format(reviews[review_num]['id'], sentiment, sentiment_score))
    

### Extract known entities

# Use the client and reviews you created previously to get named entities
entity_analysis = text_analytics_client.entities(documents=reviews)

# Print the results for each review
for review_num in range(len(reviews)):
    print(reviews[review_num]['id'])
    # Get the named entitites in this review
    entities = entity_analysis.documents[review_num].entities
    for entity in entities:
        # Only get location entitites
        if entity.type in ['DateTime','Location']:
            link = '(' + entity.wikipedia_url + ')' if entity.wikipedia_id is not None else ''
            print(' - {}: {} {}'.format(entity.type, entity.name, link))
            
            
Doc: https://docs.microsoft.com/azure/cognitive-services/text-analytics/
