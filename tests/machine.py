# Mock machine module for testing

class Pin:
    OUT = "out"
    IN = "in"
    PULL_UP = "pull_up"
    
    def __init__(self, pin, mode=None, pull=None):
        self.pin = pin
        self.mode = mode
        self.pull = pull
        self._value = 0
    
    def value(self, val=None):
        if val is None:
            return self._value
        self._value = val
    
    def on(self):
        self._value = 1
    
    def off(self):
        self._value = 0