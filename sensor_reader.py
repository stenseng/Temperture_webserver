"""
Sensor Reader Module
Handles reading DS18B20 temperature sensors
"""

from machine import Pin
import onewire
import ds18x20
import time
import ujson

class SensorReader:
    def __init__(self, pin_num):
        """Initialize the sensor reader with OneWire bus on specified pin"""
        self.pin = Pin(pin_num)
        self.ow = onewire.OneWire(self.pin)
        self.ds = ds18x20.DS18X20(self.ow)
        self.sensor_data = {}
        self.last_read_time = 0
        
    def scan_sensors(self):
        """Scan for connected DS18B20 sensors"""
        try:
            roms = self.ds.scan()
            print(f'Found {len(roms)} sensor(s): {roms}')
            return roms
        except Exception as e:
            print(f'Error scanning sensors: {e}')
            return []
    
    def read_sensors(self):
        """Read temperature from all connected sensors"""
        try:
            # Start temperature conversion on all sensors
            self.ds.convert_temp()
            # Wait for conversion to complete (750ms is typical, wait 1000ms to be safe)
            time.sleep_ms(750)
            
            roms = self.ds.scan()
            self.sensor_data = {}
            
            for rom in roms:
                try:
                    # Convert ROM address to hex string for API
                    rom_hex = self._rom_to_hex(rom)
                    temp = self.ds.read_temp(rom)
                    self.sensor_data[rom_hex] = temp
                    print(f'Sensor {rom_hex}: {temp}°C')
                except Exception as e:
                    print(f'Error reading sensor {rom}: {e}')
            
            self.last_read_time = time.time()
            return self.sensor_data
            
        except Exception as e:
            print(f'Error reading sensors: {e}')
            return {}
    
    def get_sensor_data(self):
        """Get the last read sensor data"""
        return self.sensor_data
    
    def get_sensor_list(self):
        """Get list of sensor ROM addresses as hex strings"""
        try:
            roms = self.ds.scan()
            return [self._rom_to_hex(rom) for rom in roms]
        except:
            return []
    
    @staticmethod
    def _rom_to_hex(rom):
        """Convert ROM bytes to hex string"""
        return ''.join(f'{byte:02x}' for byte in rom)
    
    @staticmethod
    def _rom_to_escaped(rom):
        """Convert ROM bytes to escaped string format for API"""
        return ''.join(f'\\x{byte:02x}' for byte in rom)
