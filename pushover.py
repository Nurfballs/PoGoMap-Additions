import json
import httplib, urllib
import time
from geopy.geocoders import Nominatim
from datetime import datetime

wanted_pokemon = None

# initialize object
def init():
    global token, user, wanted_pokemon

    #load pushover details
    with open('./config/pushoverconfig.json') as data_file:
        data = json.load(data_file)

        #get list of pokemon to send notifications for
        wanted_pokemon = _str( data["notify"] ).split(",")

        #transform to lowercase
        wanted_pokemon = [a.lower() for a in wanted_pokemon]

        #get pushover info
        token = str( data["token"] )
        user = str ( data["user"] )


# safely parse incoming strings to unicode
def _str(s):
    pokename = str(s.encode('utf-8').strip())
    return pokename.title()

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def push(title, message, nav_url):
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.urlencode({
            "token": token, 
            "user": user,
            "title": title,
            "message": message,
            "url": nav_url,
            "url_title": "Take me there!",
        }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    return

# send notification on discovered pokemon
def pokemon_found(pokemon, pos_lat, pos_lng):
    # get the pokemon name
    pokename = _str( pokemon["name"] ).lower()

    # check if it's a pokemon we give a shit about
    if not pokename in wanted_pokemon: return

    # send the notification
    print "[+] Notifier found pokemon: ", pokename
    #address = Nominatim().reverse(str(pokemon["lat"]) + "," + str(pokemon["lng"])).address
    msg_title = "A " + _str(pokemon["name"]) + " is nearby!"
    disappear_time = str(datetime.fromtimestamp(pokemon["disappear_time"]).strftime("%I:%M%p").lstrip('0'))
    nav_url = "https://www.google.com/maps/dir/" + pos_lat + "," + pos_lng + "/" + str(pokemon["lat"]) + "," + str(pokemon["lng"])
    #print "[DEBUG] Directions URL: " + nav_url

    #mytime = datetime.fromtimestamp(pokemon["disappear_time"])
    msg_body =  _str(pokemon["name"]) + " will be available until " + disappear_time + "."
    #print "[DEBUG]: " + msg_body
    #push(msg_title, msg_body, nav_url)

init()
