"""
Main Application
Raspberry Pico W Temperature Monitoring System

This application:
1. Connects to WiFi
2. Reads DS18B20 temperature sensors on Pin 12
3. Hosts a web server to display sensor temperatures
4. Pushes sensor data to a remote API
"""

import asyncio
import ntptime
import time
import _thread
from config import (
    WIFI_SSID, 
    WIFI_PASSWORD, 
    API_URL, 
    API_TOKEN, 
    SENSOR_PIN, 
    WEB_SERVER_PORT, 
    WEB_SERVER_HOST, 
    SENSOR_READ_INTERVAL, 
    API_PUSH_INTERVAL, 
    NTP_SYNC_INTERVAL
)
from wifi_manager import WiFiManager
from sensor_reader import SensorReader
from web_server import WebServer
from api_client import APIClient

# Global state
app_running = True
last_api_push = 0
last_sensor_read = 0
last_ntp_sync = 0

def sensor_api_ntp_thread(
        sensor_reader, api_client, interval_read=5, interval_push=30, interval_sync=7200
    ):
    """Background thread for reading sensors and pushing to API"""
    global last_api_push, last_sensor_read, last_ntp_sync
    
    print("Sensor and API thread started")
    
    while app_running:
        try:
            current_time = time.time()
            
            # Read sensors at regular intervals
            if current_time - last_sensor_read >= interval_read:
                print(f"\n--- Reading sensors at {time.localtime()} ---")
                sensor_reader.read_sensors()
                last_sensor_read = current_time
            
            # Push to API at regular intervals
            if current_time - last_api_push >= interval_push:
                print(f"\n--- Pushing to API at {time.localtime()} ---")
                sensor_data = sensor_reader.get_sensor_data()
                api_client.push_sensor_data(sensor_data)
                last_api_push = current_time

            # Sync time at regular intervals
            if current_time - last_ntp_sync >= interval_sync:
                print(f"\n--- Syncing NTP time at {time.localtime()} ---")
                try:
                    ntptime.settime()
                    last_ntp_sync = current_time
                except Exception as e:
                    print(f"Failed to sync NTP time: {e}")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error in sensor/API/NTP thread: {e}")
            time.sleep(5)

def main():
    """Main application entry point"""
    global app_running
    
    print("=" * 50)
    print("Raspberry Pico W Temperature Monitoring")
    print("=" * 50)
    
    try:
        # 1. Initialize WiFi
        print("\n[1/5] Initializing WiFi...")
        wifi = WiFiManager(WIFI_SSID, WIFI_PASSWORD)
        if not wifi.connect():
            print("ERROR: Failed to connect to WiFi. Check your credentials.")
            print("Update WIFI_SSID and WIFI_PASSWORD in config.py")
            return
        
        # 2 Set RTC using NTP
        print("\n[2/5] Initializing NTP time...")
        try:
            ntptime.settime()
            print("NTP time set successfully")
            print(f"Current time: {time.localtime()}")
        except Exception as e:
            print(f"Failed to set NTP time: {e}")

        # 2. Initialize sensors
        print("\n[3/5] Initializing temperature sensors...")
        sensor_reader = SensorReader(SENSOR_PIN)
        sensors = sensor_reader.scan_sensors()
        if not sensors:
            print("WARNING: No sensors found on pin {SENSOR_PIN}")
            print("Check your DS18B20 connections")
        
        # 3. Initialize API client
        print("\n[4/5] Initializing API client...")
        api_client = APIClient(API_URL, API_TOKEN)
        
        # 4. Start background thread for sensors, API, and NTP sync
        print("\n[5/5] Starting sensor and API update thread...")
        _thread.start_new_thread(
            sensor_api_ntp_thread,
            (sensor_reader, api_client, SENSOR_READ_INTERVAL, API_PUSH_INTERVAL, NTP_SYNC_INTERVAL)
        )
        
        # 5. Start web server
        print(f"\nStarting web server on http://{wifi.get_ip_address()}:{WEB_SERVER_PORT}")
        print("=" * 50)
        
        web_server = WebServer(sensor_reader, WEB_SERVER_PORT, WEB_SERVER_HOST)
        
        # This will block and run the web server
        asyncio.run(web_server.start())
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user")
        app_running = False
        time.sleep(1)
        
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\nShutting down...")
        app_running = False
        print("Done")

if __name__ == "__main__":
    main()
