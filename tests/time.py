# Mock time module for testing

import time as real_time

def sleep(seconds):
    """Mock sleep that doesn't actually wait"""
    pass

def time():
    """Return current time"""
    return real_time.time()