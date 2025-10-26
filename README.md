# Lab 7: Environment Monitor with Functions and Sensor Data

[![build](https://github.com/allegheny-college-cmpsc-100-fall-2025/lab07-starter/workflows/build/badge.svg)](https://github.com/allegheny-college-cmpsc-100-fall-2025/lab07-starter/actions)

## Overview

This lab focuses on **function organization** and **sensor data analysis** by creating an environment monitoring system. You'll learn to use functions effectively to read DHT22 sensor data, perform mathematical calculations, and generate statistical summaries of environmental conditions.

## Learning Objectives

- Practice writing and calling functions with parameters and return values
- Learn to integrate sensor hardware (DHT22) with MicroPython
- Apply mathematical calculations for data analysis and heat index
- Use conditional logic to classify environmental conditions
- Calculate and display statistical summaries (min, max, average)
- Practice error handling for hardware operations
- Organize code using modular function design

## Hardware Requirements

- Raspberry Pi Pico 2 W (or regular Pico 2)
- DHT22/AM2302 Digital Temperature Humidity Sensor Module
- Half-size breadboard (30 rows) - optional
- 3 jumper wires (female-to-male recommended)

## Program Features

Your environment monitoring system includes these **8 required functions**:

### Core Functions

1. **`read_sensor(dht_sensor)`**
   - Reads temperature and humidity from DHT22
   - Returns tuple: `(temperature_celsius, humidity_percent)`
   - Handles sensor errors gracefully

2. **`celsius_to_fahrenheit(celsius)`**
   - Converts Celsius to Fahrenheit
   - Formula: `F = (C × 9/5) + 32`
   - Handles None input

3. **`calculate_heat_index(temp_f, humidity)`**
   - Calculates "feels like" temperature
   - Uses National Weather Service heat index formula
   - Returns heat index in Fahrenheit

4. **`classify_conditions(temp_c, humidity)`**
   - Classifies temperature and humidity levels
   - Assigns comfort scores and categories
   - Returns comprehensive environmental assessment

5. **`display_reading(reading_num, temp_c, humidity, conditions)`**
   - Displays individual sensor reading with analysis
   - Shows temperature, humidity, heat index, and comfort level
   - Handles missing data gracefully

6. **`calculate_statistics(readings)`**
   - Calculates min, max, and average from all readings
   - Processes lists of temperature and humidity data
   - Returns statistical summary dictionary

7. **`display_summary(stats, location_name)`**
   - Displays comprehensive statistics for all readings
   - Shows temperature and humidity ranges and averages
   - Provides formatted summary report

8. **`wait_for_user()`**
   - Simple user interaction for pacing readings

9. **`main()`**
   - Coordinates all functions
   - Manages program flow and user experience

## Wiring Setup

### DHT22 3-Pin Module Connection

Your DHT22 sensor module has 3 pins labeled:
- **+** (VCC/Power) 
- **OUT** (Data)
- **-** (GND/Ground)

### Direct Connection Method (Recommended)

**Connect directly from DHT22 to Pico 2 W** (no breadboard needed):

1. **Female-to-Male jumper wires** work best:
   - DHT22 **+** pin → Pico 2 W **3V3** (Pin 36)
   - DHT22 **OUT** pin → Pico 2 W **GPIO 2** (Pin 4)
   - DHT22 **-** pin → Pico 2 W **GND** (Pin 38)

### Alternative: Using Breadboard

If you want to use the breadboard as a connection point:

1. **Insert Pico 2 W into breadboard** (spans the center gap)
2. **Use male-to-male jumper wires** from Pico pins to breadboard rows
3. **Use female-to-male jumper wires** from DHT22 to same breadboard rows:
   - DHT22 **+** → breadboard row connected to Pico 3V3
   - DHT22 **OUT** → breadboard row connected to Pico GPIO 2  
   - DHT22 **-** → breadboard row connected to Pico GND

### Pin Reference

```
Raspberry Pi Pico 2 W Pinout:
Pin 36 = 3V3 (3.3V Power)
Pin 4  = GPIO 2 (Digital I/O)
Pin 38 = GND (Ground)
```

## Software Setup

1. **Install Required Libraries** (if not already available):
   ```python
   # DHT library is included with MicroPython on Pico
   import dht
   import machine
   import time
   ```

2. **Test Sensor Connection**:
   ```python
   import machine
   import dht
   
   dht_pin = machine.Pin(2)
   sensor = dht.DHT22(dht_pin)
   
   sensor.measure()
   print(f"Temperature: {sensor.temperature()}°C")
   print(f"Humidity: {sensor.humidity()}%")
   ```

## Sample Output

```
Lab 7: Environment Monitor with Sensor Data
==================================================
Enter your location name: My Room
How many readings to take (1-10)? 3

Monitoring environment at 'My Room'
Taking 3 readings...

--- Reading #1 ---
Temperature: 22.5°C (72.5°F)
Humidity: 45.0%
Heat Index: 72.5°F (feels like)
Temperature: Comfortable
Humidity: Comfortable
Comfort: Very Comfortable (100/100)

Press Enter to take another reading...

--- Reading #2 ---
Temperature: 23.1°C (73.6°F)
Humidity: 48.2%
Temperature: Comfortable
Humidity: Comfortable
Comfort: Very Comfortable (100/100)

Press Enter to take another reading...

--- Reading #3 ---
Temperature: 22.8°C (73.0°F)
Humidity: 46.5%
Temperature: Comfortable
Humidity: Comfortable
Comfort: Very Comfortable (100/100)

==================================================
SUMMARY FOR 'MY ROOM'
==================================================
Total Readings: 3

TEMPERATURE:
  Minimum: 22.5°C (72.5°F)
  Maximum: 23.1°C (73.6°F)
  Average: 22.8°C (73.0°F)

HUMIDITY:
  Minimum: 45.0%
  Maximum: 48.2%
  Average: 46.6%

Monitoring complete for My Room!
You've learned to use functions for sensor data analysis!
```

## Key Features

### **Sensor Data Analysis**
- Reads temperature and humidity from DHT22 sensor
- Calculates heat index ("feels like" temperature)
- Classifies environmental conditions
- Provides comfort level assessments

### **Statistical Analysis**
- Tracks multiple readings over time
- Calculates minimum, maximum, and average values
- Displays comprehensive statistical summaries
- Uses `min()` and `max()` functions for data analysis

### **Comprehensive Function Design**
- **8 well-structured functions** for clear code organization
- **1-10 readings** for flexible data collection
- **Mathematical calculations** for heat index and statistics
- **Classification logic** for environmental assessment

## Software Setup

1. **Required Libraries** (included with MicroPython):
   ```python
   import machine
   import time
   import dht
   ```

2. **Test Sensor Connection**:
   ```python
   import machine
   import dht
   
   dht_pin = machine.Pin(2)
   sensor = dht.DHT22(dht_pin)
   
   sensor.measure()
   print(f"Temperature: {sensor.temperature()}°C")
   print(f"Humidity: {sensor.humidity()}%")
   ```

## Error Handling

Your program should handle:

- **Sensor Communication Errors**: Display error message, continue program
- **Invalid User Input**: Constrain values using `min()` and `max()`
- **Missing Data**: Handle None values gracefully in all functions
- **Mathematical Edge Cases**: Handle division by zero and invalid inputs

## Testing

The lab includes testing focused on the core functions:

- **Function Verification**: Ensures all 8 functions exist with correct signatures

Run tests with:
```bash
python3 tests/verify_functions.py
```

## Mathematical Concepts

This lab reinforces several mathematical concepts:

1. **Temperature Conversion**: Linear transformation between Celsius and Fahrenheit
2. **Heat Index Calculation**: Complex polynomial formula for "feels like" temperature
3. **Statistical Analysis**: Min, max, and average calculations
4. **Range Validation**: Using `min()` and `max()` for bounds checking
5. **Conditional Logic**: Classification based on numerical thresholds

## Debugging Tips

1. **Test sensor wiring first** - DHT22 is sensitive to connections
2. **Check function signatures** - ensure parameters match requirements
3. **Test functions individually** before running full program
4. **Handle edge cases** - test with extreme temperature/humidity values
5. **Use print statements** to trace function execution and data flow

## Common Issues

- **Sensor Read Errors**: Usually wiring or timing issues
- **Function Parameter Errors**: Check argument order and types
- **Statistical Calculation Errors**: Handle empty lists and None values
- **Import Errors**: Ensure using MicroPython on Pico

## Programming Concepts Introduced

### **Function Organization**
- Parameter passing and return values
- Data processing and mathematical operations
- Error handling strategies
- Modular code design

### **Mathematical Programming**
- Statistical calculations (min, max, average)
- Heat index formula implementation
- Conditional classification logic
- Data validation and constraint checking

## Submission

Ensure your submission includes:

- [ ] All 8 required functions implemented correctly
- [ ] Proper DHT22 sensor integration
- [ ] **Heat index calculation** using mathematical formula
- [ ] **Environmental classification** with conditional logic
- [ ] **Statistical analysis** with min, max, and average calculations
- [ ] Error handling for sensor operations and data validation
- [ ] Input validation using `min()` and `max()`
- [ ] Mathematical calculations (temperature conversion, heat index, statistics)

## Function Requirements Checklist

- [ ] `read_sensor()` - DHT22 sensor reading
- [ ] `celsius_to_fahrenheit()` - Temperature conversion
- [ ] `calculate_heat_index()` - Heat index calculation
- [ ] `classify_conditions()` - Environmental assessment
- [ ] `display_reading()` - Individual reading display
- [ ] `calculate_statistics()` - Statistical analysis
- [ ] `display_summary()` - Summary report generation
- [ ] `wait_for_user()` - User interaction
- [ ] `main()` - Program coordination

This lab provides an excellent introduction to function-based programming with practical sensor applications, mathematical calculations, and statistical analysis - all essential skills for computational problem-solving.