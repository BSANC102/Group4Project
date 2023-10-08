"""
A basic template file for using the Model class in PicoLibrary
This will allow you to implement simple Statemodels with some basic
event-based transitions.

Currently supports only 4 buttons (hardcoded to BTN1 through BTN4)
and a TIMEOUT event for internal tranisitions.

For processing your own events such as sensors, you can implement
those in your run method for transitions based on sensor events.
"""

# Import whatever Library classes you need - Model is obviously needed
import time
import random
from Model import *
from Button import *
from Counters import *
from Lights import *
from CompositeLights import *
from Sensors import *
from Buzzer import *
from Displays import *
from Counters import *

"""
FireAlarm class is a functioning fire detection system that can be utilized by 
anyone to keep their facility safe. This demo includes two sensors and a manual
alarm button that will all trigger the alarm sequence. Our sequence is designed 
to help those within the bulding evacuate and it also calls the 911 imediatly.
"""

class FireAlarm:

    def __init__(self):
        
        self._manualB = Button(12, "Manual Button", buttonhandler=None)
        self._disarmB = Button(13, "Disarm Button", buttonhandler=None)
        self._redL = Light(14,'Red LED')
        self._blueL = Light(15,'Blue LED')
        self._evacuateP = NeoPixel(pin=27, numleds=10, brightness=1)
        self._labS = DigitalSensor(28)
        self._breakroomS = DigitalSensor(26)
        self._alertBuz = PassiveBuzzer(pin=15)
        self._display = LCDDisplay(sda = 0, scl = 1, i2cid = 0)


        # 5 models
        self._model = Model(5, self, debug=True) #5 states in our state model
        

        # two buttons
        self._model.addButton(self._manualB)
        self._model.addButton(self._disarmB)


        
        # the only two state transitions done with a button pressed
        self._model.addTransition(0, [BTN1_PRESS], 2)
        self._model.addTransition(1, [NO_EVENT], 4)
        self._model.addTransition(2, [NO_EVENT], 4)
        self._model.addTransition(3, [NO_EVENT], 4)
        self._model.addTransition(4, [BTN2_PRESS], 0)


    
    #initializations
    def run(self):
        self._model.run()



    """
    stateEntered - is the handler for performing entry/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    """
    def stateEntered(self, state, event):
        if state == 0:
            # entry actions for state 0
            print('State 0 entered')
            self._display.reset()
            self._alertBuz.stop()
            self._redL.off()
            self._blueL.off()
            self._evacuateP.off()
        
        elif state == 1:
            # entry actions for state 1
            print('State 1 entered')
            self._display.showText("Fire Detected In Laboratory")

        elif state == 2:
            # entry actions for state 2
            print('State 2 entered')
            self._display.showText("Manual Alarm Pulled")
            utime.sleep(0.6)
        
        elif state == 3:
            # entry actions for state 3
            print('State 3 entered')
            self._display.showText("Fire Detected In Breakroom")


        #alarm sequence begins
        elif state == 4:
            # entry actions for state 4
            print('State 4 entered')
            self._evacuateP.run(NeoPixel.CHASES)


    """
    stateDo - the method that handles the do/actions for each state
    """
    def stateDo(self, state):
            
        # Now if you want to do different things for each state you can do it:
        if state == 0:
            # State 0 do/actions
            if self._labS.tripped():
                self._model.gotoState(1)

            elif self._breakroomS.tripped():
                self._model.gotoState(3)
        


        elif state == 4:
            self._display.showText("Dialling 911...")
            
            # police lights
            self._redL.blink()
            self._blueL.blink()
           
            # alert buzzer
            self._alertBuz.beep(tone=262)
            self._alertBuz.beep(tone=262)
            self._alertBuz.beep(tone=294)
            self._alertBuz.beep(tone=262)
            self._alertBuz.beep(tone=262)
            self._alertBuz.beep(tone=294)
            self._alertBuz.beep(tone=262)
            self._alertBuz.beep(tone=262)
            self._alertBuz.beep(tone=294)
            self._alertBuz.beep(tone=262)
            self._alertBuz.beep(tone=262)
            self._alertBuz.beep(tone=294)



    """
    stateLeft - is the handler for performing exit/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    
    This is just like stateEntered, perform only exit/actions here
    """
    def stateLeft(self, state, event):

        if state == 1:
            #exit actions for state 1
            print('State 1 left')
            self._display.reset()
        
        elif state == 2:
            #exit actions for state 2
            print('State 2 left')
            self._display.reset()
        
        elif state == 2:
            #exit actions for state 2
            print('State 2 left')
            self._display.reset()
        
        elif state == 4:
            #exit actions for state 4
            print('State 4 left')
            self._display.reset()
            self._redL.off()
            self._blueL.off()
            self._alertBuz.stop()
        

            
    

# Test your model. Note that this only runs the template class above
# If you are using a separate main.py or other control script,
# you will run your model from there.
if __name__ == '__main__':
   FireAlarm().run()