# Imports the Google Cloud client library
import json

from google.cloud import language_v1
import os

from twitterAPI import getTweets

def main():
    # grab the tweets that were retrieved with the twitterAPI
    tweets = getTweets()
    # print(tweets)

    # establishing credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'G:\My Drive\Grad School\Fall 2021\EC601 Product Design\Project2\deep-cascade-327600-a660ac53ac83.json'

    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    # nlp thresholds
    score_threshold = .2
    magnitude_threshold = .3

    # variable to store the nlp results
    nlp_results = {"data": []}

    # variable for json file that will be created
    json_file = "tweets_nlp_testing.json"

    # process each tweet and save results to json
    with open(json_file, "w") as nlp_file:

        for tweet in tweets:
            # The text to analyze
            text = tweet["text"]

            document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

            # Detects the sentiment of the text
            sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

            if sentiment.score >= score_threshold and sentiment.magnitude >= magnitude_threshold:
                nlp_results["data"].append(tweet)
            # nlp_file.write("Text: {}".format(text) + "\n")
            # nlp_file.write("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude) + "\n\n")

        # write JSON file
        nlp_file.write(json.dumps(nlp_results, indent=4))

    #print("Text: {}".format(text))
    #print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

    return json_file

if __name__ == "__main__":
    main()
