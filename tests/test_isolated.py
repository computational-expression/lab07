#!/usr/bin/env python3
"""
Isolated tests for Lab 7 functions with mock hardware.
"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from io import StringIO

# Add src and tests directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.dirname(__file__))

# Import our mock modules
import machine
import dht
import time

# Now import main with our mocks in place
import main

class TestIsolatedFunctions(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_pin = machine.Pin(2)
        self.mock_sensor = dht.DHT22(self.mock_pin)
    
    def test_read_sensor_success(self):
        """Test successful sensor reading."""
        # Set up mock sensor with known values
        self.mock_sensor.set_reading(25.5, 65.0)
        self.mock_sensor.set_error(False)
        
        temp, humidity = main.read_sensor(self.mock_sensor)
        
        self.assertEqual(temp, 25.5)
        self.assertEqual(humidity, 65.0)
    
    def test_read_sensor_error(self):
        """Test sensor reading with error."""
        # Set up mock sensor to error
        self.mock_sensor.set_error(True)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            temp, humidity = main.read_sensor(self.mock_sensor)
        
        self.assertIsNone(temp)
        self.assertIsNone(humidity)
        
        # Check error message was printed
        output = mock_stdout.getvalue()
        self.assertIn("Sensor read error", output)
    
    def test_temperature_conversion_edge_cases(self):
        """Test temperature conversion with edge cases."""
        # Test freezing point
        result = main.celsius_to_fahrenheit(0)
        self.assertEqual(result, 32.0)
        
        # Test boiling point
        result = main.celsius_to_fahrenheit(100)
        self.assertEqual(result, 212.0)
        
        # Test negative temperature
        result = main.celsius_to_fahrenheit(-40)
        self.assertEqual(result, -40.0)  # -40C = -40F
        
        # Test None
        result = main.celsius_to_fahrenheit(None)
        self.assertIsNone(result)
    
    def test_heat_index_calculations(self):
        """Test heat index calculations with various conditions."""
        # Test temperature below threshold
        result = main.calculate_heat_index(70.0, 50.0)
        self.assertEqual(result, 70.0)
        
        # Test temperature at threshold
        result = main.calculate_heat_index(80.0, 50.0)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 80.0)
        
        # Test high temperature and humidity
        result = main.calculate_heat_index(90.0, 80.0)
        self.assertGreater(result, 90.0)  # Should feel hotter
        
        # Test with None values
        self.assertIsNone(main.calculate_heat_index(None, 50.0))
        self.assertIsNone(main.calculate_heat_index(85.0, None))
    
    def test_comfort_level_boundary_conditions(self):
        """Test comfort level at boundary conditions."""
        # Test exact boundaries
        self.assertEqual(main.get_comfort_level(60.0, 50.0), "Comfortable")  # 60 is not < 60
        self.assertEqual(main.get_comfort_level(59.9, 50.0), "Too Cold")     # Just under 60
        
        self.assertEqual(main.get_comfort_level(80.0, 50.0), "Comfortable")  # 80 is not > 80
        self.assertEqual(main.get_comfort_level(80.1, 50.0), "Too Hot")      # Just over 80
        
        self.assertEqual(main.get_comfort_level(70.0, 30.0), "Comfortable")  # 30 is not < 30
        self.assertEqual(main.get_comfort_level(70.0, 29.9), "Too Dry")      # Just under 30
        
        self.assertEqual(main.get_comfort_level(70.0, 70.0), "Comfortable")  # 70 is not > 70
        self.assertEqual(main.get_comfort_level(70.0, 70.1), "Too Humid")    # Just over 70
    
    def test_alert_system_comprehensive(self):
        """Test alert system with multiple simultaneous conditions."""
        # Test multiple alerts at once
        alerts = main.check_alerts(90.0, 85.0, 100.0)
        self.assertGreaterEqual(len(alerts), 3)  # Should have temp, humidity, and heat index alerts
        
        # Test no alerts
        alerts = main.check_alerts(72.0, 50.0, 72.0)
        self.assertEqual(len(alerts), 0)
        
        # Test sensor error alert
        alerts = main.check_alerts(None, None, None)
        self.assertEqual(len(alerts), 1)
        self.assertIn("Sensor Error", alerts[0])
    
    def test_data_logging_with_timestamps(self):
        """Test data logging includes proper timestamps."""
        readings_log = []
        
        # Log first reading
        main.log_data(readings_log, 25.0, 60.0)
        time1 = readings_log[0]['timestamp']
        
        # Wait a tiny bit and log second reading
        time.sleep(0.01)  # This won't actually wait in our mock
        main.log_data(readings_log, 26.0, 65.0)
        time2 = readings_log[1]['timestamp']
        
        # Check structure
        self.assertEqual(len(readings_log), 2)
        self.assertIsInstance(time1, float)
        self.assertIsInstance(time2, float)
        
        # Check data integrity
        self.assertEqual(readings_log[1]['temp_c'], 26.0)
        self.assertEqual(readings_log[1]['humidity'], 65.0)
    
    def test_statistics_calculation_precision(self):
        """Test statistics calculation with precise values."""
        readings_log = [
            {'temp_c': 22.1, 'humidity': 45.5, 'timestamp': 1000},
            {'temp_c': 22.3, 'humidity': 46.5, 'timestamp': 1001},
            {'temp_c': 22.2, 'humidity': 47.5, 'timestamp': 1002}
        ]
        
        stats = main.calculate_statistics(readings_log)
        
        # Check exact calculations
        self.assertAlmostEqual(stats['avg_temp'], 22.2, places=3)
        self.assertAlmostEqual(stats['avg_humidity'], 46.5, places=3)
        self.assertEqual(stats['min_temp'], 22.1)
        self.assertEqual(stats['max_temp'], 22.3)
        self.assertEqual(stats['min_humidity'], 45.5)
        self.assertEqual(stats['max_humidity'], 47.5)
        self.assertEqual(stats['count'], 3)
    
    @patch('builtins.input', return_value='')
    def test_wait_for_user(self, mock_input):
        """Test wait for user function."""
        # Should not raise any exceptions
        main.wait_for_user()
        mock_input.assert_called_once()
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_functions_with_special_values(self, mock_stdout):
        """Test display functions with special values."""
        # Test display_reading with heat index same as temperature
        main.display_reading(1, 20.0, 68.0, 50.0, 68.0, "Comfortable")
        output = mock_stdout.getvalue()
        self.assertNotIn("Feels Like", output)  # Should not show feels like if same
        
        # Reset mock
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        
        # Test display_reading with different heat index
        main.display_reading(2, 30.0, 86.0, 70.0, 90.0, "Too Hot")
        output = mock_stdout.getvalue()
        self.assertIn("Feels Like: 90.0°F", output)  # Should show feels like if different

if __name__ == '__main__':
    unittest.main()