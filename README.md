# Raspberry Pico W Temperature Monitoring System

A complete IoT system for monitoring DS18B20 temperature sensors using a Raspberry Pico W, featuring a web interface and API integration.

## Features

- **Multi-sensor Support**: Read temperature from multiple DS18B20 sensors connected to GPIO pin 12
- **Web Dashboard**: Real-time temperature display accessible from any browser
- **API Integration**: Automatically push sensor data to a remote API endpoint
- **WiFi Connectivity**: Secure WiFi connection for remote monitoring
- **Async Operations**: Background thread for sensor reading and API updates

## Hardware Requirements

- Raspberry Pico W
- One or more DS18B20 temperature sensors
- 4.7kΩ pull-up resistor for the OneWire data line
- USB cable for programming

## Wiring

### DS18B20 Connection (to GPIO Pin 12):
```
DS18B20 Pin 1 (GND)   → Pico W GND
DS18B20 Pin 2 (DQ)    → Pico W GPIO 12 (with 4.7kΩ pull-up to 3.3V)
DS18B20 Pin 3 (VCC)   → Pico W 3.3V
```

## Setup Instructions

### 1. Install MicroPython on Pico W
- Download the latest Pico W firmware from [micropython.org](https://micropython.org/download/rp2-pico-w/)
- Flash it using the instructions on the website

### 2. Install Required Libraries
Copy these files to your Pico W via Thonny or similar:
- `config.py` - Configuration settings
- `main.py` - Main application
- `wifi_manager.py` - WiFi connectivity
- `sensor_reader.py` - Sensor reading
- `web_server.py` - Web server
- `api_client.py` - API client

You'll also need to install the `microdot` library for the web server:
```bash
# Via Thonny's package manager or MIP:
mip install microdot
```

### 3. Configure Settings
Edit `config.py` and update:
- `WIFI_SSID` - Your WiFi network name
- `WIFI_PASSWORD` - Your WiFi password
- `API_URL` - Your API endpoint (default: https://192.168.2.211/tempapi/)
- `API_TOKEN` - Your API authentication token
- `SENSOR_PIN` - GPIO pin number (default: 12)
- `SENSOR_READ_INTERVAL` - How often to read sensors (seconds)
- `API_PUSH_INTERVAL` - How often to push data to API (seconds)

### 4. Run the Application
- Open `main.py` in Thonny and click Run
- Or add `main.py` to `boot.py` to auto-start on power-up

## API Endpoint Format

The application sends data to your API with the following URL format:
```
https://192.168.2.211/tempapi/?token=YOUR_TOKEN&sensor1=SENSOR_ID&value1=TEMP&sensor2=SENSOR_ID&value2=TEMP&...
```

Where:
- `SENSOR_ID`: Unique hex identifier of each DS18B20
- `TEMP`: Temperature reading in Celsius (e.g., 21.8125)

## Web Interface

Access the temperature dashboard at:
```
http://<pico-ip-address>/
```

The page auto-refreshes every 5 seconds to show the latest readings.

You can also get sensor data as JSON via:
```
http://<pico-ip-address>/api/sensors
```

## Project Structure

```
First_Pico/
├── main.py              # Main application entry point
├── config.py            # Configuration file (edit this!)
├── wifi_manager.py      # WiFi connection management
├── sensor_reader.py     # DS18B20 sensor reading
├── web_server.py        # Web interface
├── api_client.py        # API communication
├── blink.py             # LED blink test (existing)
├── temp_test.py         # Sensor test (existing)
└── README.md            # This file
```

## Troubleshooting

### No sensors found
- Check your OneWire wiring on GPIO pin 12
- Verify the 4.7kΩ pull-up resistor is connected
- Check sensor power connections (3.3V and GND)

### WiFi connection fails
- Verify WIFI_SSID and WIFI_PASSWORD in config.py
- Check if WiFi network supports 2.4GHz (Pico W only supports 2.4GHz)
- Check signal strength

### API push fails
- Verify API_URL is correct and accessible
- Check API_TOKEN is valid
- Verify API endpoint accepts the parameter format
- Check network connectivity to API server

### Web server not accessible
- Note the IP address printed on startup
- Try pinging the Pico W to verify network connectivity
- Check firewall settings

## Dependencies

- **MicroPython**: Official MicroPython firmware for Pico W
- **microdot**: Web framework for MicroPython
- **urequests**: HTTP library for MicroPython (built-in)
- **onewire**: OneWire protocol (built-in)
- **ds18x20**: DS18B20 sensor driver (built-in)

## Monitoring

The application prints detailed logs including:
- WiFi connection status and IP address
- Sensor discovery and readings
- API push operations
- Web server status

Monitor these via:
- Thonny's Serial monitor
- PuTTY or other serial terminal
- Raspberry Pi Pico Web Interface

## Future Enhancements

- Data logging to flash storage
- Historical temperature graphs
- Email/SMS alerts for temperature thresholds
- MQTT support for integration with home automation systems
- SSL certificate validation for API
- Multiple WiFi network fallback

## License

Free to use and modify for your projects.
