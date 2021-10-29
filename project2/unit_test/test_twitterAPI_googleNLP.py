import pytest
from twitterAPI import getTweets
from google_nlp import main as google_nlp_main
import json

# this test checks that the Twitter API did not return an empty list
def test_getTweets():
    tweets = getTweets()
    assert len(tweets) > 0

# this test checks that google_nlp created json file and that it is not empty
def test_google_nlp_CreateJson():
    json_length = 0

    # google_nlp returns the file name of the json it created
    # if the json was successfully created then it will open
    # otherwise open() gives FileNotFoundError
    json_file = google_nlp_main()
    try:
        with open(json_file, "r") as restaurant_json:
            restaurant_data = json.load(restaurant_json)["data"]
            json_length = len(restaurant_data)
    except FileNotFoundError:
        json_file = "FileNotFoundError"

    assert json_file != "FileNotFoundError"
    assert json_length > 0