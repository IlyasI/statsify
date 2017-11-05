# Statisfy

[http://statsify.me](http://statsify.me) (Site currently NOT live)
---
Dependent on flask, json and spotipy.
```pip install spotipy flask json```

change *YOUR OWN SECRET KEY HERE* in line 10: `app.secret_key = "YOUR OWN SECRET KEY HERE"` to a secret key of your choosing.

`python statsify.py` to run.

___
Built with [Flask](http://flask.pocoo.org/) and [Spotipy]() the [Spotify web-API](https://developer.spotify.com/web-api/) Python wrapper.

[Flask Bootstrap](https://pythonhosted.org/Flask-Bootstrap/) used to achieve [Bootstrap 4](http://getbootstrap.com/) design elements and tools.

[Masonry](https://masonry.desandro.com/) used to achieve responsive image panels.


### To Do:
- Fix hiding top album images until masonry layout loaded
- Add page for raw data downloads (CSV with all top tracks/artists data)
- Add saving top tracks to a playlist(in progress)
