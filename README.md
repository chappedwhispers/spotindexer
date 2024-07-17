# spotindexer
A Python Spotify downloader

### Installation

1. Downloaded repo
2. Install these modules : `tkinter, customtkinter*, spotipy, spotdl`
3. Run `spotindexer.py` or `ctk_spotindexer.py`

**optionnal if you use only `spotindexer.py` and not `ctk_spotindexer.py`.*

### Images

Tkinter
![tkinterprev](1.png)

Customtkinter
![ctkprev](2.png)

### Known errors

When you download a music other than default MP3 (MP3 320k or FLAC or WAV ...), you can have an error like this:
The above exception was the direct cause of the following exception:           
```                                                                               
+--------------------- Traceback (most recent call last) ---------------------+
| C:\Users\NGRT\AppData\Local\Programs\Python\Python312\Lib\site-packages\spo |
| tipy\client.py:311 in _internal_call                                        |
|                                                                             |
|    308                 reason = retry_error.args[0].reason                  |
|    309             except (IndexError, AttributeError):                     |
|    310                 reason = None                                        |
| >  311             raise SpotifyException(                                  |
|    312                 429,                                                 |
|    313                 -1,                                                  |
|    314                 f"{request.path_url}:\n Max Retries",                |
+-----------------------------------------------------------------------------+
SpotifyException: http status: 429, code:-1 -                                  
/v1/artists/7hJcb9fa4alzcOq3EaNPoG:
```
There are not any solution to remediate it but you can retry download.


Another error is "yt-dlprovider error". Like the first, there are not any solution to remediate it but you can retry download.
