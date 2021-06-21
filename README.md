# Welcome to Berta voice assistant!
Bachelor thesis: Development and evalution of a voice assistant system based on open source compoments.

Berta is a Raspberry Pi local voice assistant system based on open
source components.

See the following instructions on how to work with it.

Deployement on Linux or Raspberry Pi Hosting.
Raspberry Pi with Raspbian, official distribution from the Raspberry Pi Foundation.
Use a fresh setup SD Card with Raspbian for using Berta.

Installing Berta on Raspberry Pi by cloning the application directly from its git repository:
$ git clone https://github.com/PassionPlus/berta.git

Create virtual environment in berta file and install all the package dependencies.
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt


Run Berta:
$ flask run


Updating database:
By every change on the application models an updated has to be done, so a new migration needs to be generated:
(venv) $ flask db migrate -m "your message"
Applieing migration to the database:
(venv) $ flask db upgrade

Switching database:
If a  database server such as MySQL wants to be userd. Change the DATABASE_URL in the config.py to your chosen one.
The database in the databse server has to be created befor running (venv) $ flask db upgrade

Note:
By using this in a production environment it is recommended to change the SECRET_KEY in the config.py.


The self-signed certificate was given in this repo for demonstration purposes.
It is suggested that the self-signed certificate is replaced with a real one, so that the browser does not warn about the site.

Helpfull Links:
Learn Python:
It's a Python 2 tutorial, but for the 
overview it's enough. 
https://developers.google.com/edu/python

Learn Flask:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


DeepSpeech:
https://deepspeech.readthedocs.io/en/r0.9/
https://www.hackster.io/dmitrywat/offline-speech-recognition-on-raspberry-pi-4-with-respeaker-c537e7


