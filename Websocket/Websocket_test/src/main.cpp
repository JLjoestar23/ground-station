#include <WiFi.h>
#include <ESPAsyncWebServer.h>

// Replace with your network credentials
const char* ssid = "WS_server_test";

// Create an AsyncWebServer object on port 80
AsyncWebServer server(80);
// Create a WebSocket object on the path "/ws"
AsyncWebSocket ws("/ws");

// Example radio data (this would be dynamically updated in a real scenario)
int msg_number = 0;

// Function to send radio data to all connected WebSocket clients
void notifyClients() {
  String jsonData = String("{\"message\":") + random()/10000 + "}";
  ws.textAll(jsonData);
}

// WebSocket event handler
void onWebSocketEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, 
                      AwsEventType type, void *arg, uint8_t *data, size_t len) {
  if (type == WS_EVT_CONNECT) {
    Serial.println("WebSocket client connected");
  } else if (type == WS_EVT_DISCONNECT) {
    Serial.println("WebSocket client disconnected");
  }
}

void setup() {
  // Start Serial Monitor
  Serial.begin(115200);
   
  delay(250);

  // Connect to Wi-Fi
  WiFi.mode(WIFI_AP);
  if (!WiFi.softAP(ssid)) {
    Serial.print("Soft AP creation failed.");
    while (1);
  }
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  Serial.println("Server started");

  // Attach the WebSocket event handler
  ws.onEvent(onWebSocketEvent);
  server.addHandler(&ws);

  // Start the server
  server.begin();
}

void loop() {
  delay(100);
  // Simulate radio data updates
  Serial.println(msg_number);
  msg_number += 1;

  // Notify WebSocket clients with the updated data
  notifyClients();
}