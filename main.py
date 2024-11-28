from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv('.env.local')

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_artist_name():
    artist_name = input("Enter the name of the artist: ")
    return artist_name

def get_token(): 
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    # POST request to get token
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_headers(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist (token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_headers(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist found")
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_headers(token)
    query = "?market=US"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


token = get_token()
result = search_for_artist(token, artist_name= get_artist_name())
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']} (Album: {song['album']['name']})")


'''
Future improvements:
- Add error handling
- Add more features like getting the albums, related ariists, create a playlist with the top songs, etc
- Add more interactivity to the user with menu options

def main():
    
    while True:
        print("\nMenu:")
        print("1. Search for Artist")
        print("2. Fetch Top Tracks")
        print("3. Fetch Albums")
        print("4. Find Related Artists")
        print("5. Create Playlist")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            artist_name = get_artist_name()
            artist = search_for_artist(token, artist_name)
        elif choice == "2" and artist:
            songs = get_songs_by_artist(token, artist["id"])
            for idx, song in enumerate(songs):
                print(f"{idx + 1}. {song['name']} (Album: {song['album']['name']})")
        elif choice == "6":
            break
        else:
            print("Invalid choice or no artist selected.")

main()

'''
