# Imports the Google Cloud client library
from google.cloud import language_v1
import os

#establishing credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'G:\My Drive\Grad School\Fall 2021\EC601 Product Design\Project2\deep-cascade-327600-a660ac53ac83.json'

# Instantiates a client
client = language_v1.LanguageServiceClient()

# The text to analyze
text = "Boston isn't only rich in history, but it has a great foodie scene too. That famous Boston Cream Pie? I have the best of the best right here to make it easy for you! Best Boston Cream Pie in Boston + My Favorite! https://t.co/ARVctLu7D0 | #boston #dessert #food |  https://t.co/TFIpIzF9uA"
document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

print("Text: {}".format(text))
print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))