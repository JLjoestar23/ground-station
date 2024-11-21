import requests
import websocket
import json

# Replace with your ESP32 IP
ESP32_IP = "192.168.4.1"

def get_radio_data():
    """Fetch radio data from the ESP32 HTTP endpoint."""
    url = f"http://{ESP32_IP}/radio-data"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Radio Data:", response.json())
        else:
            print("Failed to fetch data:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

def on_message(ws, message):
    """Handle incoming WebSocket messages."""
    try:
        data = json.loads(message)
        print("Real-time Data:", data)
    except json.JSONDecodeError:
        print("Invalid message received:", message)

def on_error(ws, error):
    """Handle WebSocket errors."""
    print("WebSocket Error:", error)

def on_close(ws, close_status_code, close_msg):
    """Handle WebSocket closure."""
    print("WebSocket Closed")

def connect_websocket():
    """Connect to the ESP32 WebSocket for real-time data."""
    ws_url = f"ws://{ESP32_IP}/ws"
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    print("Fetching initial data...")
    get_radio_data()

    print("\nConnecting to WebSocket for real-time updates...")
    connect_websocket()
