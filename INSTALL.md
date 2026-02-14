# Installation Instructions for Pico W

## Step 1: Flash MicroPython Firmware

1. Download the Pico W firmware from: https://micropython.org/download/rp2-pico-w/
2. Hold the BOOTSEL button while plugging in USB to enter bootloader mode
3. Copy the downloaded .uf2 file to the RPI-RP2 USB drive
4. Pico W will reboot with MicroPython installed

## Step 2: Install Required Libraries

Using Thonny IDE (recommended):
1. Open Thonny
2. Go to Tools → Manage packages
3. Search for and install: `microdot`
4. Thonny will install it to your Pico W

Alternatively, using `mip` (built into MicroPython):
1. Open Thonny's serial monitor
2. Run:
   ```python
   import mip
   mip.install("microdot")
   ```

## Step 3: Upload Files to Pico W

Using Thonny:
1. Click "View" menu → "Files"
2. Right-click each Python file and select "Upload to /"
3. Upload order:
   - config.py (EDIT THIS FIRST with your WiFi details!)
   - wifi_manager.py
   - sensor_reader.py
   - api_client.py
   - web_server.py
   - main.py

Using command line (if mip supports it):
```bash
mpremote cp config.py :
mpremote cp wifi_manager.py :
mpremote cp sensor_reader.py :
mpremote cp api_client.py :
mpremote cp web_server.py :
mpremote cp main.py :
```

## Step 4: Configure WiFi and API

Edit `config.py` on the Pico W in Thonny:
- Change WIFI_SSID to your WiFi network name
- Change WIFI_PASSWORD to your WiFi password
- Update API_URL, API_TOKEN if needed

## Step 5: Run the Application

Option A - Run once (for testing):
1. Open main.py in Thonny
2. Click the Run button (▶)
3. Watch the output for connection status

Option B - Auto-start on boot:
1. Create a new file called `boot.py`
2. Add this content:
   ```python
   import main
   ```
3. Upload boot.py to the Pico W
4. The app will start automatically when powered on

## Accessing the Web Interface

1. Note the IP address printed in the Thonny console
2. Open a web browser (on same WiFi network)
3. Go to: http://YOUR_PICO_IP_ADDRESS/
4. You should see the temperature dashboard

## Getting Sensor IDs

The sensor IDs will be printed to the console when the app starts.
They look like: `283c1e050000b3` or similar hex strings.

Use these IDs to identify sensors in your API calls.

## Preventing Brownout on Startup

If you get brownout errors, add this to config.py:
```python
import machine
machine.freq(125_000_000)  # Reduce CPU frequency
```

## Testing Without API

You can test the sensor reading and web interface without configuring the API:
1. Set API_PUSH_INTERVAL to a very high number (e.g., 999999)
2. Or comment out the API push in main.py
3. The web interface will still work

---

For detailed setup, see README.md
