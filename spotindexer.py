import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import threading
import subprocess

spotify_client_id = 'UR_CLIENT_ID'
spotify_client_secret = 'UR_CLIENT_SECRET'
client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_spotify():
    query = entry_search.get().strip()
    search_type = search_type_var.get().lower()

    if not query:
        messagebox.showwarning("Warning", "Please enter a search query.")
        return

    try:
        listbox_results.delete(0, tk.END)
        if search_type == 'all':
            results_albums = sp.search(q=query, type='album', limit=10)
            results_tracks = sp.search(q=query, type='track', limit=10)
            results_playlists = sp.search(q=query, type='playlist', limit=10)
            items_albums = results_albums['albums']['items']
            items_tracks = results_tracks['tracks']['items']
            items_playlists = results_playlists['playlists']['items']
            display_results(items_albums, 'album')
            display_results(items_tracks, 'track')
            display_results(items_playlists, 'playlist')
        elif search_type == 'albums':
            results = sp.search(q=query, type='album', limit=10)
            items = results['albums']['items']
            display_results(items, 'album')
        elif search_type == 'tracks':
            results = sp.search(q=query, type='track', limit=10)
            items = results['tracks']['items']
            display_results(items, 'track')
        elif search_type == 'playlists':
            results = sp.search(q=query, type='playlist', limit=10)
            items = results['playlists']['items']
            display_results(items, 'playlist')
        else:
            messagebox.showwarning("Attention", "Search type not available.")
            return

    except Exception as e:
        messagebox.showerror("Error", f"Error during the Spotify search: {str(e)}")

def display_results(items, result_type):
    for item in items:
        if result_type == 'album':
            artists = ', '.join([artist['name'] for artist in item['artists']])
            title = item['name']
            album = title
            release_date = item['release_date']
            link = item['external_urls']['spotify']
            item_text = f"{artists} - {title} (Album - {release_date})"
        elif result_type == 'track':
            artists = ', '.join([artist['name'] for artist in item['artists']])
            title = item['name']
            album = item['album']['name']
            release_date = item['album']['release_date']
            link = item['external_urls']['spotify']
            item_text = f"{artists} - {title} ({album} - {release_date})"
        elif result_type == 'playlist':
            creator = item['owner']['display_name']
            title = item['name']
            link = item['external_urls']['spotify']
            item_text = f"{creator} - Playlist : {title}"
        else:
            continue

        listbox_results.insert(tk.END, item_text)
        result_data[item_text] = {'link': link}

def download_music():
    selected_indices = listbox_results.curselection()
    if not selected_indices:
        messagebox.showwarning("Attention", "Please select a track or an album to download.")
        return

    selected_item = listbox_results.get(selected_indices[0])
    selected_link = result_data[selected_item]['link']

    def run_download():
        try:
            if '/album/' in selected_link:
                download_album(selected_link)
            else:
                download_track(selected_link)
        except Exception as e:
            write_to_console(f"Error during downloading: {str(e)}\n")

    threading.Thread(target=run_download).start()

def download_album(album_link):
    try:
        album_id = album_link.split('/album/')[1].split('?')[0]
        tracks = sp.album_tracks(album_id)['items']
        for track in tracks:
            track_url = track['external_urls']['spotify']
            download_command = build_download_command(track_url)
            run_command(download_command)
    except Exception as e:
        write_to_console(f"Error during album download: {str(e)}\n")

def download_track(track_link):
    download_command = build_download_command(track_link)
    run_command(download_command)

def build_download_command(link):
    format_choice = format_var.get().replace(" ", "").lower()
    if "mp3" in format_choice:
        bitrate = format_choice.split("mp3")[1]
        return f"spotdl {link} --bitrate {bitrate}"
    else:
        return f"spotdl {link} --format {format_choice}"

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        write_to_console(line)
    for line in process.stderr:
        write_to_console(line)
    process.wait()
    write_to_console(f"Finished command with output code {process.returncode}\n")

def write_to_console(message):
    console_output.config(state=tk.NORMAL)
    console_output.insert(tk.END, message)
    console_output.yview(tk.END)
    console_output.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Spotindexer")

root.resizable(False, False)

frame_search = ttk.Frame(root)
frame_search.pack(pady=10)

label_search = ttk.Label(frame_search, text="Search:")
label_search.grid(row=0, column=0, padx=10, pady=5)

entry_search = ttk.Entry(frame_search, width=40)
entry_search.grid(row=0, column=1, padx=10, pady=5)

search_type_var = tk.StringVar()
search_type_var.set("All")

label_search_type = ttk.Label(frame_search, text="Search type:")
label_search_type.grid(row=0, column=2, padx=10, pady=5)

search_type_menu = ttk.OptionMenu(frame_search, search_type_var, "All", "All", "Albums", "Tracks", "Playlists")
search_type_menu.grid(row=0, column=3, padx=10, pady=5)

button_search = ttk.Button(frame_search, text="Search", command=search_spotify)
button_search.grid(row=0, column=4, padx=10, pady=5)

frame_results = ttk.Frame(root)
frame_results.pack(pady=10)

listbox_results = tk.Listbox(frame_results, width=80, height=10)
listbox_results.grid(row=0, column=0, padx=10, pady=5)

frame_format = ttk.Frame(root)
frame_format.pack(pady=10)

format_var = tk.StringVar()
format_var.set("MP3 192kbps")

label_format = ttk.Label(frame_format, text="Output format:")
label_format.grid(row=0, column=0, padx=10, pady=5)

format_menu = ttk.OptionMenu(frame_format, format_var, "MP3 192k", "MP3 192k", "MP3 320k", "FLAC", "WAV", "OGG")
format_menu.grid(row=0, column=1, padx=10, pady=5)

button_download = ttk.Button(root, text="Download", command=download_music)
button_download.pack(pady=10)

frame_console = ttk.Frame(root)
frame_console.pack(pady=10)

console_output = scrolledtext.ScrolledText(frame_console, width=80, height=10, state=tk.DISABLED)
console_output.pack(padx=10, pady=5)

result_data = {}

root.mainloop()
