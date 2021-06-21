from app import app, db, berta
# python top-level script that defines the Flask application instance
from app.models import User, DeepSpeechLog
from app.berta_deepspeech import main_internal
import threading
import time
import pyaudio 


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'DeepSpeechLog': DeepSpeechLog}

def flask_thread():
    app.run(host='0.0.0.0', port="3000", debug=True, use_reloader=False)

def berta_thread():
    #berta.pa = pyaudio.PyAudio()

    while True:
        try:
            output = berta.run()
            #if(db and model):
            log = DeepSpeechLog(question=output[0], answer=output[1])
            db.session.add(log)
            db.session.commit()
                
        except KeyboardInterrupt:
            print("exiting")
            break

#berta_main = threading.Thread(target=berta_thread, daemon=True)
#berta_main.start()
#berta_thread()

#main_internal("bumblebee", db, DeepSpeechLog)

if __name__ == "__main__":
    berta_web = threading.Thread(target=flask_thread, daemon=True)
    berta_web.start()
    
    #berta.main()
    #app.run()
    #while True:
    #    try:
    #        output = berta.run()
            #if(db and model):
    #        log = DeepSpeechLog(question=output[0], answer=output[1])
    #        db.session.add(log)
    #        db.session.commit()
                
    #    except KeyboardInterrupt:
    #        print("exiting")
    #        break
    main_internal("bumblebee", db, DeepSpeechLog)
    # multiple keywords can be given through comma seprated string
    # !!! MUST BE STRING, not list, etc
    #main_internal("bumblebee,hey berta", db, DeepSpeechLog)
