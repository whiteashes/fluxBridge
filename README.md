# fluxBridge
Flask server app that handles POST requests from an inFlux database and then forwards obtained data to a Telegram bot. <br/></br>
You simply have to setup a Python virtual environment in which you must install flask libs through pip (or pip3); after that, you've to run the script in command line making sure you've set the path environment variable for Flask:</br>

```FLASK_APP=app.py```

</br>

The name must be the same with the script one. Then type:</br>

```
flask run
```

</br>

You can edit the IP address inside the script or running it this way: </br>

```flask run -h <ipAddr>```
  
</br>
Default is localhost.
