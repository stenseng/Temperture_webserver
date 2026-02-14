# Configuration file for Pico W Temperature Monitoring Project

# WiFi Configuration
WIFI_SSID = "Your_wifi_ssid"
WIFI_PASSWORD = "Something_secret"

# API Configuration
API_URL = "https://192.168.1.5/tempapi/"
API_TOKEN = "long_token_string_here"

# Sensor Configuration
SENSOR_PIN = 12  # GPIO pin for OneWire DS18B20 sensors

# Server Configuration
WEB_SERVER_PORT = 80
WEB_SERVER_HOST = "0.0.0.0"

# Update intervals (in seconds)
SENSOR_READ_INTERVAL = 5  # How often to read sensors
API_PUSH_INTERVAL = 30    # How often to push data to API
NTP_SYNC_INTERVAL = 7200  # How often to sync time with NTP (2 hours)
