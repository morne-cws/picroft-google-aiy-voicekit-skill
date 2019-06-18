"""
skill picroft-google-aiy-voicekit
Copyright (C) 2018  Andreas Lorensen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from mycroft import MycroftSkill
from mycroft.messagebus.message import Message

import time
import RPi.GPIO as GPIO


class PicroftGoogleAiyVoicekit(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        try:
            # pin 23 is the GPIO pin the button is attached to
            # pin 4 is the GPIO pin the LED light is attached to
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(4, GPIO.OUT)
            GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            pass
        except GPIO.error:
            self.log.warning("Cant initialize GPIO - skill will not load")
            self.speak_dialog("error.initialise")
        finally:
            self.schedule_repeating_event(self.handle_button,
                                          None, 0.1, 'GoogleAIY')
            self.add_event('recognizer_loop:record_begin',
                           self.handle_listener_started)
            self.add_event('recognizer_loop:record_end',
                           self.handle_listener_ended)

    def handle_button(self, message):
        longpress_threshold = 2
        if not GPIO.input(23):
            pressed_time = time.time()
            while GPIO.input(23):
                time.sleep(0.2)
            pressed_time = time.time()-pressed_time
            if pressed_time < longpress_threshold:
                self.bus.emit(Message("mycroft.mic.listen"))
            else:
                self.bus.emit(Message("mycroft.stop"))
                
    def handle_boot_finished(self):
        # code to excecute when active listening begins...
        GPIO.output(4, GPIO.HIGH)


def create_skill():
    return PicroftGoogleAiyVoicekit()
