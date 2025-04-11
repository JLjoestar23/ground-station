import websocket
import json
import time
from collections import deque

# A simple queue to buffer messages
message_queue = deque()

def on_message(ws, message):
    """Handle incoming WebSocket messages."""
    try:
        data = json.loads(message)
        print("Received Data:", data)
        message_queue.append(data)  # Add message to the queue
    except json.JSONDecodeError:
        print("Invalid message received:", message)

def process_messages():
    """Process messages in the queue."""
    while message_queue:
        message = message_queue.popleft()  # Get the next message in the queue
        print(f"Processing: {message}")
        # Add any additional processing logic here

def on_error(ws, error):
    """Handle WebSocket errors."""
    print("WebSocket Error:", error)

def on_close(ws, close_status_code, close_msg):
    """Handle WebSocket closure."""
    print("WebSocket Closed")

def connect_websocket():
    """Connect to the ESP32 WebSocket for real-time data."""
    ws_url = "ws://192.168.4.1/ws"
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    print("Connecting to WebSocket for real-time updates...")
    connect_websocket()
    while True:
        process_messages()  # Periodically process the messages in the queue
        time.sleep(0.1)  # Adjust the sleep time if needed
