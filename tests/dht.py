# Mock dht module for testing

class DHT22:
    def __init__(self, pin):
        self.pin = pin
        self._temp = 22.5  # Default temperature
        self._humidity = 45.0  # Default humidity
        self._should_error = False
    
    def measure(self):
        if self._should_error:
            raise Exception("Sensor communication error")
    
    def temperature(self):
        if self._should_error:
            raise Exception("Sensor communication error")
        return self._temp
    
    def humidity(self):
        if self._should_error:
            raise Exception("Sensor communication error")
        return self._humidity
    
    # Test helper methods
    def set_reading(self, temp, humidity):
        """Set mock sensor reading for testing"""
        self._temp = temp
        self._humidity = humidity
    
    def set_error(self, error_state):
        """Set mock sensor to error state for testing"""
        self._should_error = error_state