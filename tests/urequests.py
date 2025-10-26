# Mock urequests module for testing

class MockResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {
            "location": {"name": "London"},
            "current": {
                "temp_c": 20.0,
                "humidity": 60.0,
                "condition": {"text": "Clear"}
            }
        }
    
    def json(self):
        return self._json_data
    
    def close(self):
        pass

def get(url, timeout=10):
    """Mock HTTP GET request"""
    return MockResponse()