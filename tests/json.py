# Mock json module for testing

def loads(json_string):
    """Mock JSON loads function"""
    # For testing, return a simple dict
    return {
        "location": {"name": "London"},
        "current": {
            "temp_c": 20.0,
            "humidity": 60.0,
            "condition": {"text": "Clear"}
        }
    }

def dumps(obj):
    """Mock JSON dumps function"""
    return str(obj)