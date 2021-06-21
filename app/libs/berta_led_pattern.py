#!/usr/bin/env python

# Copyright (C) 2017 Seeed Technology Limited
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


import numpy
import time
try:
    import queue as Queue
except ImportError:
    import Queue as Queue


#class GoogleHomeLedPattern(object):
class BertaLedPattern(object):
    def __init__(self, show=None):
        #48 numbers are used for the 12 led array
        #4 values per LED
        blue = numpy.array([0,0,0,4])
        white = numpy.array([0,4,4,4])
        red = numpy.array([0,4,0,0])
        self.basis = numpy.array([0] * 4 * 12)
        #print(self.basis)
        #numpy.put(self.basis, 0 , self.led1)
        self.basis[0:4] = white
        self.basis[4:8] = red
        self.basis[8:12] = red
        self.basis[12:16] = red
        self.basis[16:20] = red
        self.basis[20:24] = red
        self.basis[24:28] = white
        self.basis[28:32] = blue
        self.basis[32:36] = blue
        self.basis[36:40] = blue
        self.basis[40:44] = blue
        self.basis[44:48] = blue
        #print("after")
        #print(self.basis)
        # original google colors
        # self.basis[0 * 4 + 1] = 2
        # self.basis[3 * 4 + 1] = 1
        # self.basis[3 * 4 + 2] = 1
        # self.basis[6 * 4 + 2] = 2
        # self.basis[9 * 4 + 3] = 2

        #self.basis[0 * 4 + 1] = 3
        #self.basis[0 * 4 + 2] = 3
        #self.basis[0 * 4 + 3] = 3
        #self.basis[3 * 4 + 2] = 3
        #self.basis[6 * 4 + 2] = 0
        #self.basis[9 * 4 + 3] = 0
        print(self.basis)
        self.pixels = self.basis * 24
        print(self.pixels)

        if not show or not callable(show):
            def dummy(data):
                pass
            show = dummy

        self.show = show
        self.stop = False

    def wakeup(self, direction=0):
        position = int((direction + 15) / 30) % 12

        basis = numpy.roll(self.basis, position * 8)
        for i in range(1, 25):
            pixels = basis * i
            self.show(pixels)
            time.sleep(0.005)

        pixels =  numpy.roll(pixels, 4)
        self.show(pixels)
        time.sleep(0.1)

        for i in range(2):
            new_pixels = numpy.roll(pixels, 4)
            self.show(new_pixels * 0.5 + pixels)
            pixels = new_pixels
            time.sleep(0.1)

        self.show(pixels)
        self.pixels = pixels

    def listen(self):
        pixels = self.pixels
        while not self.stop:
            for i in range(1, 25):
                self.show(pixels * i / 24)
                time.sleep(0.025)
                if self.stop : break

    def think(self):
        pixels = self.pixels

        while not self.stop:
            pixels = numpy.roll(pixels, 4)
            self.show(pixels)
            time.sleep(0.2)

        t = 0.1
        for i in range(0, 5):
            pixels = numpy.roll(pixels, 4)
            self.show(pixels * (8 - i) / 8)
            time.sleep(t)
            t /= 2

        self.pixels = pixels

    def speak(self):
        pixels = self.pixels
        step = 1
        brightness = 5
        while not self.stop:
            self.show(pixels * brightness / 24)
            time.sleep(0.02)

            if brightness <= 5:
                step = 1
                time.sleep(0.4)
            elif brightness >= 24:
                step = -1
                time.sleep(0.4)

            brightness += step

    def off(self):
        self.show([0] * 4 * 12)


