#!/usr/bin/env python3
"""
Comprehensive tests for Lab 7 environment monitoring functions.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock the hardware modules
sys.modules['machine'] = MagicMock()
sys.modules['dht'] = MagicMock()

import main

class TestEnvironmentMonitorFunctions(unittest.TestCase):
    
    def test_celsius_to_fahrenheit(self):
        """Test temperature conversion from Celsius to Fahrenheit."""
        # Test normal conversions
        self.assertAlmostEqual(main.celsius_to_fahrenheit(0), 32.0, places=1)
        self.assertAlmostEqual(main.celsius_to_fahrenheit(100), 212.0, places=1)
        self.assertAlmostEqual(main.celsius_to_fahrenheit(25), 77.0, places=1)
        self.assertAlmostEqual(main.celsius_to_fahrenheit(-10), 14.0, places=1)
        
        # Test None input
        self.assertIsNone(main.celsius_to_fahrenheit(None))
    
    def test_calculate_heat_index(self):
        """Test heat index calculation."""
        # Test high temperature (above 80°F)
        result = main.calculate_heat_index(85.0, 60.0)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 80)
        
        # Test low temperature (below 80°F) - should return same temp
        result = main.calculate_heat_index(75.0, 60.0)
        self.assertEqual(result, 75.0)
        
        # Test None inputs
        self.assertIsNone(main.calculate_heat_index(None, 60.0))
        self.assertIsNone(main.calculate_heat_index(85.0, None))
        self.assertIsNone(main.calculate_heat_index(None, None))
    
    def test_get_comfort_level(self):
        """Test comfort level determination."""
        # Test comfortable conditions
        self.assertEqual(main.get_comfort_level(72.0, 50.0), "Comfortable")
        
        # Test temperature extremes
        self.assertEqual(main.get_comfort_level(55.0, 50.0), "Too Cold")
        self.assertEqual(main.get_comfort_level(85.0, 50.0), "Too Hot")
        
        # Test humidity extremes
        self.assertEqual(main.get_comfort_level(72.0, 25.0), "Too Dry")
        self.assertEqual(main.get_comfort_level(72.0, 75.0), "Too Humid")
        
        # Test None inputs
        self.assertEqual(main.get_comfort_level(None, 50.0), "Unknown")
        self.assertEqual(main.get_comfort_level(72.0, None), "Unknown")
    
    def test_check_alerts(self):
        """Test environmental alert system."""
        # Test normal conditions - no alerts
        alerts = main.check_alerts(72.0, 50.0, 72.0)
        self.assertEqual(len(alerts), 0)
        
        # Test high temperature
        alerts = main.check_alerts(90.0, 50.0, 95.0)
        self.assertTrue(any("HIGH TEMPERATURE" in alert for alert in alerts))
        
        # Test low temperature
        alerts = main.check_alerts(50.0, 50.0, 50.0)
        self.assertTrue(any("LOW TEMPERATURE" in alert for alert in alerts))
        
        # Test high humidity
        alerts = main.check_alerts(72.0, 85.0, 72.0)
        self.assertTrue(any("HIGH HUMIDITY" in alert for alert in alerts))
        
        # Test low humidity
        alerts = main.check_alerts(72.0, 20.0, 72.0)
        self.assertTrue(any("LOW HUMIDITY" in alert for alert in alerts))
        
        # Test heat index warning
        alerts = main.check_alerts(85.0, 50.0, 95.0)
        self.assertTrue(any("HEAT INDEX" in alert for alert in alerts))
        
        # Test sensor error
        alerts = main.check_alerts(None, None, None)
        self.assertTrue(any("Sensor Error" in alert for alert in alerts))
    
    def test_log_data(self):
        """Test data logging functionality."""
        readings_log = []
        
        # Test valid data logging
        main.log_data(readings_log, 25.0, 60.0)
        self.assertEqual(len(readings_log), 1)
        self.assertEqual(readings_log[0]['temp_c'], 25.0)
        self.assertEqual(readings_log[0]['humidity'], 60.0)
        self.assertIn('timestamp', readings_log[0])
        
        # Test None data - should not log
        main.log_data(readings_log, None, 60.0)
        main.log_data(readings_log, 25.0, None)
        self.assertEqual(len(readings_log), 1)  # Should still be 1
    
    def test_calculate_statistics(self):
        """Test statistics calculation."""
        # Test empty log
        stats = main.calculate_statistics([])
        self.assertIsNone(stats)
        
        # Test with data
        readings_log = [
            {'temp_c': 20.0, 'humidity': 40.0, 'timestamp': 1234567890},
            {'temp_c': 25.0, 'humidity': 60.0, 'timestamp': 1234567891},
            {'temp_c': 30.0, 'humidity': 50.0, 'timestamp': 1234567892}
        ]
        
        stats = main.calculate_statistics(readings_log)
        self.assertIsNotNone(stats)
        self.assertEqual(stats['count'], 3)
        self.assertAlmostEqual(stats['avg_temp'], 25.0, places=1)
        self.assertEqual(stats['min_temp'], 20.0)
        self.assertEqual(stats['max_temp'], 30.0)
        self.assertAlmostEqual(stats['avg_humidity'], 50.0, places=1)
        self.assertEqual(stats['min_humidity'], 40.0)
        self.assertEqual(stats['max_humidity'], 60.0)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_reading(self, mock_stdout):
        """Test reading display function."""
        # Test valid reading
        main.display_reading(1, 25.0, 77.0, 60.0, 80.0, "Comfortable")
        output = mock_stdout.getvalue()
        self.assertIn("Reading #1", output)
        self.assertIn("25.0°C", output)
        self.assertIn("77.0°F", output)
        self.assertIn("60.0%", output)
        self.assertIn("Comfortable", output)
        
        # Reset mock
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        
        # Test sensor error
        main.display_reading(2, None, None, None, None, "Unknown")
        output = mock_stdout.getvalue()
        self.assertIn("Sensor Error", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_summary(self, mock_stdout):
        """Test summary display function."""
        # Test with None stats
        main.display_summary(None)
        output = mock_stdout.getvalue()
        self.assertIn("No data available", output)
        
        # Reset mock
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        
        # Test with stats
        stats = {
            'count': 5,
            'avg_temp': 25.0,
            'min_temp': 20.0,
            'max_temp': 30.0,
            'avg_humidity': 50.0,
            'min_humidity': 40.0,
            'max_humidity': 60.0
        }
        
        main.display_summary(stats)
        output = mock_stdout.getvalue()
        self.assertIn("5 readings", output)
        self.assertIn("25.0°C", output)
        self.assertIn("20.0°C to 30.0°C", output)

if __name__ == '__main__':
    unittest.main()