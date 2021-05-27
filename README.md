# berta
Raspberry pi local voice assistant

Installing Berta:

Running Berta:

Updating database:
By every change on the application models an updated has to be done, so a new migration needs to be generated:
(venv) $ flask db migrate -m "your message"
Applieing migration to the database:
(venv) $ flask db upgrade

Switching database:
If a  database server such as MySQL wants to be userd. Change the DATABASE_URL to your chosen one.
The database in the databse server has to be created befor running (venv) $ flask db upgrade

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


