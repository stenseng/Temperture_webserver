"""
Web Server Module
Hosts a simple webpage displaying sensor temperatures
"""

import asyncio
import ujson
from microdot import Microdot

class WebServer:
    def __init__(self, sensor_reader, port=80, host="0.0.0.0"):
        """Initialize the web server"""
        self.sensor_reader = sensor_reader
        self.port = port
        self.host = host
        self.app = Microdot()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup HTTP routes"""
        
        @self.app.route('/')
        async def index(request):
            """Main page showing temperature readings"""
            html = self._generate_html()
            return html, {'Content-Type': 'text/html'}
        
        @self.app.route('/api/sensors')
        async def api_sensors(request):
            """API endpoint returning sensor data as JSON"""
            data = self.sensor_reader.get_sensor_data()
            return ujson.dumps(data)
    
    def _generate_html(self):
        """Generate HTML for the temperature display page"""
        sensor_data = self.sensor_reader.get_sensor_data()
        
        # Build table rows for each sensor
        rows = ""
        if sensor_data:
            for sensor_id, temp in sensor_data.items():
                rows += f"""
                <tr>
                    <td>{sensor_id}</td>
                    <td>{temp:.2f}°C</td>
                </tr>
                """
        else:
            rows = "<tr><td colspan='2'>No sensors found</td></tr>"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Raspberry Pico W - Temperature Sensors</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                h1 {{
                    color: #333;
                    text-align: center;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background-color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                th {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 12px;
                    text-align: left;
                }}
                td {{
                    padding: 10px;
                    border-bottom: 1px solid #ddd;
                }}
                tr:hover {{
                    background-color: #f9f9f9;
                }}
                .refresh {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
            <script>
                setInterval(function() {{
                    location.reload();
                }}, 5000);
            </script>
        </head>
        <body>
            <h1>Temperature Monitoring</h1>
            <table>
                <tr>
                    <th>Sensor ID</th>
                    <th>Temperature</th>
                </tr>
                {rows}
            </table>
            <div class="refresh">
                <p>Auto-refreshing every 5 seconds...</p>
            </div>
        </body>
        </html>
        """
        return html
    
    async def start(self):
        """Start the web server"""
        #print(f"Starting web server on host={self.app.host}, port={self.app.port}")
        #self.app.run(debug=False) #, host=self.app.host, port=self.app.port)
        self.server = asyncio.create_task(self.app.start_server(debug=True, host='0.0.0.0', port=80))
        await self.server

    def stop(self):
        """Stop the web server"""
        self.app.shutdown()
