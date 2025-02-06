import requests
import websocket
import json

class DataHandler:
    def __init__(self):
        self.ESP32_IP = "192.168.4.1" # IP Address
        self.ws_url = f"ws://{self.ESP32_IP}/ws"
        self.ws = websocket.WebSocketApp(self.ws_url, on_message = self.on_message, on_error = self.on_error, on_close = self.on_close)

    def get_radio_data(self):
        """
        Fetch radio data from the ESP32 HTTP endpoint.
        """
        url = f"http://{self.ESP32_IP}/radio-data"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Radio Data:", response.json())
            else:
                print("Failed to fetch data:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def connect_websocket(self):
        """
        Connect to the ESP32 WebSocket for real-time data.
        """
        self.ws.run_forever()

    def disconnect_websocket(self):
        if self.ws:
            print("Disconnecting Websocket")
            self.ws.close()

    def on_message(self, ws, message):
        """
        Handle incoming WebSocket messages.
        """
        try:
            data = json.loads(message)
            print("Real-time Data:", data)
        except json.JSONDecodeError:
            print("Invalid message received:", message)

    def on_error(self, ws, error):
        """
        Handle WebSocket errors.
        """
        print("WebSocket Error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        """
        Handle WebSocket closure.
        """
        print("WebSocket Closed")

if __name__ == "__main__":
    data = DataHandler()
    print("\nConnecting to WebSocket for real-time updates...")
    data.connect_websocket()
