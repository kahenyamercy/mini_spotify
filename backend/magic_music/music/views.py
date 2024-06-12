from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = requests.post(url, headers=headers, data=data)
    
    if result.status_code != 200:
        return None

    json_result = result.json()
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def top_artists():
    token = get_token()
    if not token:
        return []

    url = "https://api.spotify.com/v1/artists"
    headers = get_auth_header(token)
    artist_ids = "4tZwfgrHOc3mvqYlEYSvVi,1uNFoZAHBGtllmzznpCI3s,66CXWjxzNUsdJxJ2JdwvnR"  # Example artist IDs

    params = {
        "ids": artist_ids
    }

    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()

    artists_info = []
    if 'artists' in response_data:
        for artist in response_data['artists']:
            name = artist.get('name', 'No Name')
            avatar_url = artist.get('images', [{}])[0].get('url', 'No URL')
            artist_id = artist.get('id', 'No ID')
            artists_info.append((name, avatar_url, artist_id))

    return artists_info

def top_tracks():
    token = get_token()
    if not token:
        return []

    url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbLRQDuF5jeBp"  # Spotify Global Top 50 playlist ID
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers)
    data = response.json()
    track_details = []

    if 'tracks' in data and 'items' in data['tracks']:
        for item in data['tracks']['items']:
            track = item['track']
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name'] if track['artists'] else None
            cover_url = track['album']['images'][0]['url'] if track['album']['images'] else None

            track_details.append({
                'id': track_id,
                'name': track_name,
                'artist': artist_name,
                'cover_url': cover_url
            })

    return track_details

def get_audio_details(query):
    token = get_token()
    if not token:
        return []

    url = f"https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    audio_details = []

    if response.status_code == 200:
        data = response.json()
        if 'tracks' in data and 'items' in data['tracks']:
            track = data['tracks']['items'][0]
            audio_details.append(track['preview_url'])
            audio_details.append(track['duration_ms'])

    return audio_details

def get_track_image(track_id):
    token = get_token()
    if not token:
        return ""

    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'album' in data and 'images' in data['album']:
            return data['album']['images'][0]['url']
    return ""

def music(request, pk):
    track_id = pk

    token = get_token()
    if not token:
        return HttpResponse("Could not retrieve token", status=500)

    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        track_name = data.get("name")
        artists_list = data.get("artists", [])
        first_artist_name = artists_list[0].get("name") if artists_list else "No artist found"

        audio_details_query = track_name + " " + first_artist_name
        audio_details = get_audio_details(audio_details_query)
        audio_url = audio_details[0]
        duration_text = str(audio_details[1]) + " ms"

        track_image = get_track_image(track_id)

        context = {
            'track_name': track_name,
            'artist_name': first_artist_name,
            'audio_url': audio_url,
            'duration_text': duration_text,
            'track_image': track_image,
        }
    return render(request, 'music.html', context)

@login_required(login_url='login')
def index(request):
    artists_info = top_artists()
    top_track_list = top_tracks()

    # divide the list into three parts
    first_six_tracks = top_track_list[:6]
    second_six_tracks = top_track_list[6:12]
    third_six_tracks = top_track_list[12:18]

    context = {
        'artists_info': artists_info,
        'first_six_tracks': first_six_tracks,
        'second_six_tracks': second_six_tracks,
        'third_six_tracks': third_six_tracks,
    }
    return render(request, 'index.html', context)

def search(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']

        token = get_token()
        if not token:
            return HttpResponse("Could not retrieve token", status=500)

        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header(token)
        params = {
            "q": search_query,
            "type": "track",
            "limit": 10
        }

        response = requests.get(url, headers=headers, params=params)
        track_list = []

        if response.status_code == 200:
            data = response.json()
            search_results_count = data["tracks"]["total"]
            tracks = data["tracks"]["items"]

            for track in tracks:
                track_name = track["name"]
                artist_name = track["artists"][0]["name"]
                duration = track["duration_ms"]
                trackid = track["id"]
                track_image = get_track_image(trackid)

                track_list.append({
                    'track_name': track_name,
                    'artist_name': artist_name,
                    'duration': duration,
                    'trackid': trackid,
                    'track_image': track_image,
                })
        context = {
            'search_results_count': search_results_count,
            'track_list': track_list,
        }

        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')

def profile(request, pk):
    artist_id = pk

    token = get_token()
    if not token:
        return HttpResponse("Could not retrieve token", status=500)

    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        name = data["name"]
        monthly_listeners = data["followers"]["total"]
        header_url = data["images"][0]["url"]

        top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
        params = {"market": "US"}
        top_tracks_response = requests.get(top_tracks_url, headers=headers, params=params)
        top_tracks_data = top_tracks_response.json()
        
        top_tracks = []
        if 'tracks' in top_tracks_data:
            for track in top_tracks_data['tracks']:
                trackid = track["id"]
                trackname = track["name"]
                trackimage = get_track_image(trackid)

                track_info = {
                    "id": trackid,
                    "name": trackname,
                    "duration_ms": track["duration_ms"],
                    "play_count": track["popularity"],
                    "track_image": trackimage
                }

                top_tracks.append(track_info)

        artist_data = {
            "name": name,
            "monthlyListeners": monthly_listeners,
            "headerUrl": header_url,
            "topTracks": top_tracks,
        }
    else:
        artist_data = {}
    return render(request, 'profile.html', artist_data)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
        
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in 
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:    
        return render(request, 'signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
