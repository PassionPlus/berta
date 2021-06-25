#
# Copyright 2018 Picovoice Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#from halo import Halo
import time, logging
import argparse
import os
import glob
import struct
import sys
from datetime import datetime
from threading import Thread

import deepspeech
from .libs.audio_tools import VADAudio
#from .libs import audio_tools
import numpy as np
import pyaudio
import soundfile
import wave
from io import BytesIO
from picotts import PicoTTS
from .libs.pixels import Pixels, pixels
from .actionprovider import ActionProvider
#from app import pa

#sys.path.append(os.path.join(os.path.dirname(__file__), 'binding/python'))
#sys.path.append(os.path.join(os.path.dirname(__file__), 'resources/util/python'))

from pvporcupine import * #Porcupine
#from util import *

logging.basicConfig(level=logging.INFO)

#os.close(sys.stderr.fileno())

class BertaDeepSpeech(Thread):
    """
    Class for wake word detection (aka Porcupine) library. It creates an input audio stream from a microphone,
    monitors it, and upon detecting the specified wake word(s) prints the detection time and index of wake word on
    console. 
    """
    def __init__(
            self,
            library_path,
            model_path,
            keyword_paths,
            sensitivities,
            input_device_index=None,
            output_path=None):

        """
        Constructor.

        :param library_path: Absolute path to Porcupine's dynamic library.
        :param model_file_path: Absolute path to the model parameter file.
        :param keyword_file_paths: List of absolute paths to keyword files.
        :param sensitivities: Sensitivity parameter for each wake word. For more information refer to
        'include/pv_porcupine.h'. It uses the
        same sensitivity value for all keywords.
        :param input_device_index: Optional argument. If provided, audio is recorded from this input device. Otherwise,
        the default audio input device is used.
        :param output_path: If provided recorded audio will be stored in this location at the end of the run.
        """

        super(BertaDeepSpeech, self).__init__()

        self._library_path = library_path
        self._model_path = model_path
        self._keyword_paths = keyword_paths
        self._sensitivities = sensitivities
        self._input_device_index = input_device_index
        self.db_model = None
        self.pt = PicoTTS()
        self.pa = pyaudio.PyAudio()

        self._output_path = output_path
        if self._output_path is not None:
            self._recorded_frames = []
            
        #Load DeepSpeech model
        print('Initializing model...')
        dirname = os.path.dirname(os.path.abspath(__file__))
        model_name = glob.glob(os.path.join(dirname,'libs/*.tflite'))[0]
        logging.info("Model: %s", model_name)
        self.model = deepspeech.Model(model_name)
        try:
            scorer_name = glob.glob(os.path.join(dirname,'*.scorer'))[0]
            logging.info("Language model: %s", scorer_name)
            self.model.enableExternalScorer(scorer_name)
        except Exception as e:
            pass        

    def set_model(self, db_model):
        self.db_model = db_model

    def transcribe(self):
        # Start audio with VAD
        vad_audio = VADAudio(aggressiveness=1,
                             device=None,
                             input_rate=16000,
                             file=None)
        print("Listening (ctrl-C to exit)...")
        frames = vad_audio.vad_collector()

        # Stream from microphone to DeepSpeech using VAD
        #spinner = Halo(spinner='line')
        stream_context = self.model.createStream()
        #wav_data = bytearray()
        listening = False
        for frame in frames:
            if frame is not None:
                if not listening:
                    pixels.listen()
                    listening = True
        #        if spinner: spinner.start()
                logging.debug("streaming frame")
                stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
                #if ARGS.savewav: wav_data.extend(frame)
            else:
                if listening:
                    listening = False
                    pixels.think()
               # if spinner: spinner.stop()
                logging.debug("end utterence")
                #if ARGS.savewav:
                #    vad_audio.write_wav(os.path.join(ARGS.savewav, datetime.now().strftime("savewav_%Y-%m-%d_%H-%M-%S_%f.wav")), wav_data)
                #    wav_data = bytearray()
                text = stream_context.finishStream()
                print("Recognized: %s" % text)


                log = (text, self.analyze(text))
                return (1, log)

                if 'stop recording' in text:
                    vad_audio.destroy()
                    #break
                    return 1
                stream_context = self.model.createStream()

    def find_action(self,phrase):
        words = phrase.lower().split()
        default = [x for x in ActionProvider.plugins if 'default' in x.categories][0]
        for word in words:
            action = [x for x in ActionProvider.plugins if word in x.categories]
            if action:
                return action[0]()
        return default()

    def analyze(self, phrase):
        """Method that analyzes the phrase given, speaks and returns the answer"""
        # find the correct action to take
        action = self.find_action(phrase)
        # perform the action and get the answer
        answer = action.perform()
        # speek the answer
        self.speek(answer)
        # return answer for saving into database
        return answer

    def test_phrase(self, phrase):
        """Method used in web application to test apis maually"""
        # find the correct action to take
        action = self.find_action(phrase)
        # perform the action and get the answer
        answer = action.perform()
        # return answer for saving into database
        return answer

    def speek(self, answer):
        """Method that generates the audio data and plays it on the microphone"""
        self.pa = pyaudio.PyAudio()
        # 1kb of data at a time
        chunk = 1024
        # create the picotts wav
        wavs = self.pt.synth_wav(str(answer))
        # open wav for processing
        wav = wave.open(BytesIO(wavs))
        # create audio stream for output
        stream = self.pa.open(format = self.pa.get_format_from_width(wav.getsampwidth()),
            channels = wav.getnchannels(),
            rate = wav.getframerate(),
            output = True)
        data = wav.readframes(chunk)
        pixels.speak()
        print("speaking here")


        while data:
            #print(data)
            stream.write(data)
            data = wav.readframes(chunk)
        print("done speaking")
        pixels.off()
        stream.stop_stream()
        stream.close()
        self.pa.terminate()


    def run(self):
        """
         Creates an input audio stream, initializes wake word detection (Porcupine) object, and monitors the audio
         stream for occurrences of the wake word(s). It prints the time of detection for each occurrence and index of
         wake word.
         """

        num_keywords = len(self._keyword_paths)

        keywords = list()
        for x in self._keyword_paths:
            keywords.append(os.path.basename(x).replace('.ppn', '').replace('_compressed', '').split('_')[0])

        print('listening for:')
        for keyword, sensitivity in zip(keywords, self._sensitivities):
            print('- %s (sensitivity: %f)' % (keyword, sensitivity))

        porcupine = None
        pa = None
        audio_stream = None
        try:
            porcupine = Porcupine(
                library_path=self._library_path,
                model_path=self._model_path,
                keyword_paths=self._keyword_paths,
                sensitivities=self._sensitivities)

            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length,
                input_device_index=self._input_device_index)

            while True:
                pcm = audio_stream.read(porcupine.frame_length)

                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                if self._output_path is not None:
                    self._recorded_frames.append(pcm)

                result = porcupine.process(pcm)

                if result >= 0:
                    print('[%s] Detected %s' % (str(datetime.now()), keywords[result]))
                    pixels.wakeup()
                    audio_stream.close()
                    ds_result = self.transcribe()
                    #if self.transcribe():
                    if ds_result[0]:
                                    audio_stream = pa.open(
                                    rate=porcupine.sample_rate,
                                    channels=1,
                                    format=pyaudio.paInt16,
                                    input=True,
                                    frames_per_buffer=porcupine.frame_length,
                                    input_device_index=self._input_device_index)
                    return ds_result[1]

        except KeyboardInterrupt:
            print('stopping ...')
            raise KeyboardInterrupt
        finally:
            if porcupine is not None:
                porcupine.delete()

            if audio_stream is not None:
                audio_stream.close()

            if pa is not None:
                pa.terminate()

            if self._output_path is not None and len(self._recorded_frames) > 0:
                recorded_audio = np.concatenate(self._recorded_frames, axis=0).astype(np.int16)
                soundfile.write(self._output_path, recorded_audio, samplerate=porcupine.sample_rate, subtype='PCM_16')

            pixels.off()

    _AUDIO_DEVICE_INFO_KEYS = ['index', 'name', 'defaultSampleRate', 'maxInputChannels']

    @classmethod
    def show_audio_devices_info(cls):
        """ Provides information regarding different audio devices available. """

        pa = pyaudio.PyAudio()

        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            print(', '.join("'%s': '%s'" % (k, str(info[k])) for k in cls._AUDIO_DEVICE_INFO_KEYS))

        pa.terminate()

def berta_factory(keywords):
    """Berta object creator with sane defaults for use outside the application"""
    library_path = LIBRARY_PATH
    keyword_paths = None
    kws = [x.strip() for x in keywords.split(',')]
    if all(x in KEYWORDS for x in kws):
        keyword_paths = [KEYWORD_PATHS[x] for x in kws]
    else:
        raise ValueError(
            'selected keywords are not available by default. available keywords are: %s' % ', '.join(KEYWORDS))
    model_path = MODEL_PATH
    sensitivities=0.5
    if isinstance(sensitivities, float):
        sensitivities = [sensitivities] * len(keyword_paths)

    output_path = None
    input_device_index = None
    return BertaDeepSpeech(
        library_path=library_path,
        model_path=model_path,
        keyword_paths=keyword_paths,
        sensitivities=sensitivities,
        output_path=output_path,
        input_device_index=None)
    
def main_internal(keywords, db, model):
    berta = berta_factory(keywords)
    print("MAIN")
    while True:
        try:
            output = berta.run()
            print(output)
            print(db)
            print(model)
            #if(db and berta.db_model):
            log = model(question=output[0], answer=output[1])
            print(output[0])
            print(output[1])
            db.session.add(log)
            db.session.commit()
                
        except KeyboardInterrupt:
            print("exiting")
            return 1

if __name__ == '__main__':
    #main()
    main_internal('bumblebee,computer')
