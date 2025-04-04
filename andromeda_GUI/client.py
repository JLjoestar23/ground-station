import requests
import websocket
import json
import threading

class DataHandler:
    def __init__(self):
        self.ESP32_IP = "192.168.4.1"  # IP Address
        self.ws_url = f"ws://{self.ESP32_IP}/ws"
        self.ws = None
        self.data = None  # Store the latest data received
        self.running = False  # Control the WebSocket thread
        self.thread = None  # Thread for WebSocket communication

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
        Start the WebSocket connection in a separate thread.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_websocket, daemon=True)
            self.thread.start()
            print("WebSocket thread started.")

    def disconnect_websocket(self):
        """
        Stop the WebSocket connection and thread.
        """
        self.running = False
        if self.ws:
            print("Disconnecting WebSocket...")
            self.ws.close()
        if self.thread:
            self.thread.join()
            print("WebSocket thread stopped.")

    def _run_websocket(self):
        """
        Internal method to run the WebSocket connection.
        """
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.run_forever()

    def on_message(self, ws, message):
        """
        Handle incoming WebSocket messages.
        """
        try:
            self.data = json.loads(message)  # Update the latest data
            #print(self.data)  # Debugging: Print the received data
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

    def get_data(self):
        """
        Return the latest data received from the WebSocket.
        """
        return self.data


if __name__ == "__main__":
    # Example usage
    data_handler = DataHandler()
    data_handler.connect_websocket()
    print(data_handler.get_data())