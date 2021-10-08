import folium
import webbrowser
import json

# variable to store json data
restaurant_data = []

#get json data
json_file = "tweets_nlp_processed.json"
with open(json_file, 'r') as restaurant_json:
    restaurant_data = json.load(restaurant_json)["data"]
    #print(restaurant_data)

# create map center point @ Boston Common
center_lat = 42.35915456045076
center_long = -71.06572151456187
foodMap = folium.Map(location=[center_lat, center_long], zoom_start=10)
tooltip = "Awesome Food<br>Click Me!"

for restaurant in restaurant_data:

    # check for valid latitude, zero means that there is no geo data linked to tweet
    if restaurant["location"]["lat"] != 0:
        name = restaurant["location"]["rest_name"]
        addr = restaurant["location"]["address"]
        user = restaurant["name"]

        # only hyperlink in tweet text
        if restaurant["text"][0:4] == "http":
            tweet = "<a href=\"" + restaurant["text"] + "\">" + restaurant["text"] + "</a>"

        # this is grabbing the last 23 chars in the string to check if it is a url
        elif restaurant["text"][-23::][0:4] == "http":
            url1 = "<a href=\"" + restaurant["text"][-23::] + "\">" + restaurant["text"][-23::] + "</a>"
            shortenedText = restaurant["text"][0:-24]

            # check if there is a second url
            if shortenedText[-23::][0:4] == "http":
                url2 = "<a href=\"" + shortenedText[-23::] + "\">" + shortenedText[-23::] + "</a>"

                tweet = shortenedText[0:-23] + url2 + " " + url1
            else:
                tweet = restaurant["text"][0:-23] + url1
        else:
            tweet = restaurant["text"]

        lat = restaurant["location"]["lat"]
        long = restaurant["location"]["long"]
        popupText = f"<b>{name}</b><br><i>{addr}</i><br><br><b>{user}</b> tweeted:<br>{tweet}"
        folium.Marker([lat, long], popup=popupText, tooltip=tooltip, icon=folium.Icon(color="blue", icon="info-sign")).add_to(foodMap)

# save map to html
html_file = "foodMap.html"
foodMap.save(html_file)

# open map in web browser
webbrowser.open_new_tab(html_file)
