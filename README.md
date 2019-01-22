# Statisfy

Responsive Flask and Bootstrap built site that displays your top Spotify artists and tracks in a pretty mosiac. Time ranges include over all time, 6 months, and 1 month.

Instructions to run:
---
Step 1: Statsify is dependent on flask, flask-bootstrap, spotipy, and appdirs:
```pip install spotipy flask flask-bootstrap appdirs```

Step 2: create config.json based on config_example.json in the main statsify directory, where 'ClientSecret' and 'ClientID' are obtained from https://developer.spotify.com/dashboard/applications. You must make a new application and put the client id and client secret within the parenthesis of the file. The 'SecretKey' field should then be set to a random string of your choosing.

{

	"ClientSecret": "12345678910", 
	
	"ClientID": "12345678910",
	
	"SecretKey": "You can set this to whatever you want."
	
}

Step 3: `python statsify.py` to run. The site will be hosted locally at 127.0.0.1:8000. On the first visit you will be prompted to login through Spotify Oauth.

Screenshots:
---
![Statsify Screenshot 3](https://github.com/IlyasI/statsify/blob/master/screenshots/screen3.jpg)

---
![Statsify Screenshot 1](https://github.com/IlyasI/statsify/blob/master/screenshots/screen1.jpg)

---
![Statsify Screenshot 2](https://github.com/IlyasI/statsify/blob/master/screenshots/screen2.png)

___
Built with [Flask](http://flask.pocoo.org/) and [Spotipy]() the [Spotify web-API](https://developer.spotify.com/web-api/) Python wrapper.

[Flask Bootstrap](https://pythonhosted.org/Flask-Bootstrap/) used to achieve [Bootstrap 4](http://getbootstrap.com/) design elements and tools.

[Masonry](https://masonry.desandro.com/) used to achieve responsive image panels.

