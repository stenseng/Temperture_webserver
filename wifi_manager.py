"""
WiFi Manager Module
Handles WiFi connection and network setup
"""

import network
import time

class WiFiManager:
    def __init__(self, ssid, password):
        """Initialize WiFi manager"""
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.connected = False
    
    def connect(self, timeout=10):
        """
        Connect to WiFi network
        
        Args:
            timeout: Maximum time to wait for connection in seconds
        
        Returns:
            True if connected, False otherwise
        """
        try:
            self.wlan.active(True)
            
            # Check if already connected
            if self.wlan.isconnected():
                print(f"Already connected to {self.ssid}")
                self.connected = True
                return True
            
            print(f"Connecting to WiFi: {self.ssid}")
            self.wlan.connect(self.ssid, self.password)
            
            # Wait for connection
            start_time = time.time()
            while not self.wlan.isconnected():
                if time.time() - start_time > timeout:
                    print(f"WiFi connection timeout after {timeout} seconds")
                    self.connected = False
                    return False
                time.sleep(0.5)
            
            # Print network info
            ifconfig = self.wlan.ifconfig()
            print(f"WiFi connected!")
            print(f"IP address: {ifconfig[0]}")
            print(f"Subnet mask: {ifconfig[1]}")
            print(f"Gateway: {ifconfig[2]}")
            print(f"DNS: {ifconfig[3]}")
            
            self.connected = True
            return True
            
        except Exception as e:
            print(f"Error connecting to WiFi: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from WiFi"""
        try:
            self.wlan.disconnect()
            self.wlan.active(False)
            self.connected = False
            print("WiFi disconnected")
            return True
        except Exception as e:
            print(f"Error disconnecting from WiFi: {e}")
            return False
    
    def is_connected(self):
        """Check if connected to WiFi"""
        return self.wlan.isconnected()
    
    def get_ip_address(self):
        """Get current IP address"""
        if self.is_connected():
            return self.wlan.ifconfig()[0]
        return None
