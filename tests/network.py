# Mock network module for testing

WLAN = None
STA_IF = "sta_if"

class WLAN:
    def __init__(self, interface):
        self.interface = interface
        self._connected = False
        self._config = ["192.168.1.100", "255.255.255.0", "192.168.1.1", "8.8.8.8"]
    
    def active(self, state=None):
        if state is not None:
            return state
        return True
    
    def isconnected(self):
        return self._connected
    
    def connect(self, ssid, password):
        # Simulate successful connection for testing
        self._connected = True
    
    def ifconfig(self):
        return self._config