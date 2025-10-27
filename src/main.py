"""
Lab 7: Environment Monitor with Functions and Sensor Data
CMPSC 100 - Computational Expression

Purpose: Create a simple environment monitoring system using functions
to organize code and integrate DHT22 sensor for data collection.
"""

import machine
import time
import dht

# TODO: Implement functions to organize your code:
# 
# 1. A function to read temperature and humidity from DHT22 sensor
#    - Take sensor measurement and get readings
#    - Check if readings are valid and in reasonable ranges
#    - Return readings or None values if error
#
# 2. A function to convert Celsius to Fahrenheit
#    - Apply conversion formula: (celsius * 9/5) + 32
#    - Handle None input appropriately
#
# 3. A function to assess comfort level based on temperature and humidity
#    - Use if/elif/else to categorize comfort levels
#    - Consider both temperature and humidity in assessment
#    - Return comfort assessment string
#
# 4. A function to classify environmental conditions
#    - Classify temperature into categories (Cold, Cool, Comfortable, Warm, Hot)
#    - Classify humidity into categories (Dry, Comfortable, Humid, Very Humid)
#    - Return tuple with both classifications (temp_category, humidity_category)
#
# 5. A function to display a single sensor reading with analysis
#    - Print reading header with reading number
#    - Convert temperature to Fahrenheit and get comfort level
#    - Display all information in formatted output
#
# 6. A function to calculate statistics from multiple readings
#    - Separate valid temperature and humidity values using loops
#    - Calculate min, max, and average for both temperature and humidity
#    - Return statistics as tuple (temp_min, temp_max, temp_avg, humidity_min, humidity_max, humidity_avg, reading_count)
#
# 7. A function to display summary statistics
#    - Display formatted header with location name
#    - Show temperature and humidity statistics in organized format
#    - Include additional math operations for requirements
#
# 8. A function to wait between readings
#    - Print message about waiting
#    - Use time.sleep() to pause for a few seconds

def main():
    """Main function to run the environment monitoring system."""
    
    print("Lab 7: Environment Monitor with Sensor Data")
    print("=" * 50)
    
    # Initialize DHT22 sensor on GPIO pin 2
    dht_pin = machine.Pin(2)
    dht_sensor = dht.DHT22(dht_pin)
    
    # Get user preferences
    location_name = input("Enter your location name: ")
    
    # Get number of readings with simple validation
    readings_input = input("How many readings to take (1-10)? ")
    readings_count = int(readings_input)
    
    # Use min and max to constrain the value
    readings_count = max(1, min(10, readings_count))
    
    print(f"\nMonitoring environment at '{location_name}'")
    print(f"Taking {readings_count} readings...")
    
    # Store all readings for statistics
    all_readings = []
    
    for reading_num in range(1, readings_count + 1):
        # TODO: Call your sensor reading function here
        temp_c, humidity = None, None  # Replace with your function call
        
        # TODO: Call your classification function here
        conditions = None  # Replace with your function call
        
        # TODO: Call your display function here
        print(f"\n--- Reading #{reading_num} ---")
        print("Sensor functions not yet implemented")
        
        # Store reading for statistics
        all_readings.append((temp_c, humidity))
        
        # Wait before next reading (except last one)
        if reading_num < readings_count:
            # TODO: Call your wait function here
            print("\nWaiting 3 seconds before next reading...")  # Replace with your function
            time.sleep(3)
            time.sleep(2)
    
    # TODO: Call your statistics calculation function here
    stats = None  # Replace with your function call
    
    # TODO: Call your summary display function here
    
    print(f"\nMonitoring complete for {location_name}!")
   
if __name__ == "__main__":
    main()