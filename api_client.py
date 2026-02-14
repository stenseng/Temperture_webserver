"""
API Client Module
Handles pushing sensor data to remote API
"""

import urequests
import ujson
import time

class APIClient:
    def __init__(self, api_url, api_token):
        """Initialize API client"""
        self.api_url = api_url
        self.api_token = api_token
    
    def push_sensor_data(self, sensor_data):
        """
        Push sensor data to API
        
        Args:
            sensor_data: Dictionary with sensor hex strings as keys and temps as values
        
        Returns:
            True if successful, False otherwise
        """
        if not sensor_data:
            print("No sensor data to push")
            return False
        
        try:
            # Build query parameters
            params = {"token": self.api_token}
            
            # Add each sensor to parameters
            sensor_list = list(sensor_data.items())
            for idx, (sensor_id, temp) in enumerate(sensor_list, 1):
                params[f"sensor{idx}"] = sensor_id
                params[f"value{idx}"] = temp
            
            # Build URL with parameters
            url = self._build_url(params)
            
            print(f"Pushing data to API: {url}")
            
            # Make the request
            response = urequests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"API push successful: {response.text}")
                response.close()
                return True
            else:
                print(f"API push failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                response.close()
                return False
                
        except Exception as e:
            print(f"Error pushing to API: {e}")
            return False
    
    def _build_url(self, params):
        """Build URL with query parameters"""
        url = self.api_url
        
        # Add query parameters
        query_parts = []
        for key, value in params.items():
            # URL encode the values
            query_parts.append(f"{key}={self._url_encode(str(value))}")
        
        if query_parts:
            url += "?" + "&".join(query_parts)
        
        return url
    
    @staticmethod
    def _url_encode(value):
        """Simple URL encoding"""
        # For this specific API format, we need to handle special characters
        # The API expects escaped hex sequences like \\x97
        return value
