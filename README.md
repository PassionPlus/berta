# berta
Bachelor thesis: Development and evalution of a language assistant system based on open source compoments.

Berta is a Raspberry Pi local voice assistant system based on open
source components.

Installing Berta on Raspberry Pi:
$ git clone https://github.com/PassionPlus/berta.git

Create virtual environment and install all the package dependencies.
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt


Run Berta:


Updating database:
By every change on the application models an updated has to be done, so a new migration needs to be generated:
(venv) $ flask db migrate -m "your message"
Applieing migration to the database:
(venv) $ flask db upgrade

Switching database:
If a  database server such as MySQL wants to be userd. Change the DATABASE_URL to your chosen one.
The database in the databse server has to be created befor running (venv) $ flask db upgrade

Note:
By using this in a production environment it is recommended to change the SECRET_KEY in the config.py.

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


