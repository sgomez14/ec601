import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
#bearer_token = os.environ.get("BEARER_TOKEN")

with open("bearerToken.txt","r") as bearerTokenFile:
    bearer_token = bearerTokenFile.read()


search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}

twitter_handles = []

# read txt file with usernames of people in Boston that tweet about restaurants
with open("food_twitter.txt", 'r') as twitter_file:
    for line in twitter_file:
        #print(line.rstrip())
        twitter_handles.append("from:" + line.strip("@").rstrip() + " OR ")
    twitter_handles[-1] = twitter_handles[-1].strip(" OR ") #remove the last OR from the last handle
    #print(twitter_handles)

    #creating one string with all the twitter handles
    query_handles = ""
    query_handles = query_handles.join(twitter_handles)
    #print(query_handles)



max_results = 100
possible_keywords = "(#food OR #restaurant OR #foodie OR #delicious )(Boston)"
keyword = f"({query_handles})(-is:retweet)"
#print(keyword)
tweet_fields = 'author_id,geo'
expansions = 'author_id'
query_params = {'query': keyword,
                'tweet.fields': tweet_fields,
                'max_results': max_results,
                'expansions': expansions
                }

tweets = []

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def getTweets():
    json_response = connect_to_endpoint(search_url, query_params)
    #print(json.dumps(json_response, indent=4, sort_keys=True))

    users = []

    #get all of the users that appear in the results
    for user in json_response["includes"]["users"]:
        users.append(user)
    #print(users)

    for tweet in json_response["data"]:

        #append username to tweet record
        for user in users:
            if tweet["author_id"] == user["id"]:
                tweet["name"] = user["name"]
                tweet["location"] = {"rest_name": "","address": "", "lat": 0, "long": 0}

        #add tweet record to list
        tweets.append(tweet)

    if len(tweets) > 0:
        print("Tweet results saved to list")
    else:
        print("Error: Tweets did not save to list")

    #print(tweets)

    return tweets

def main():
    getTweets()

if __name__ == "__main__":
    main()