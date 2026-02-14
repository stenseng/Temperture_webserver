"""
Quick Start Example - Simple Test
Run this to test your sensors before running the full application
"""

from config import SENSOR_PIN
from sensor_reader import SensorReader
import time

print("Starting sensor test...\n")

# Create sensor reader
sr = SensorReader(SENSOR_PIN)

# Scan for sensors
print("Scanning for DS18B20 sensors on GPIO pin {}...".format(SENSOR_PIN))
sensors = sr.scan_sensors()

if not sensors:
    print("ERROR: No sensors found!")
    print("Check your DS18B20 wiring:")
    print("  - Data pin (DQ) to GPIO 12")
    print("  - GND to Pico W GND")
    print("  - VCC to Pico W 3.3V")
    print("  - 4.7k pull-up resistor on data line")
else:
    print(f"Found {len(sensors)} sensor(s)!\n")
    
    # Read sensors multiple times
    for i in range(5):
        print(f"Reading #{i+1}:")
        sr.read_sensors()
        data = sr.get_sensor_data()
        for sensor_id, temp in data.items():
            print(f"  {sensor_id}: {temp}°C")
        print()
        time.sleep(2)
    
    print("Sensor test completed successfully!")
    print("\nNext steps:")
    print("1. Edit config.py with your WiFi credentials")
    print("2. Run main.py to start the full application")
