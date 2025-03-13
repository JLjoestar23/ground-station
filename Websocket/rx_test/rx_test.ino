#include "radio_class.h"
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>
#include <ArduinoJson.h>

Radio radio;

const char* ssid = "WS_test";

// Create an AsyncWebServer object on port 80
AsyncWebServer server(80);
// Create a WebSocket object on the path "/ws"
AsyncWebSocket ws("/ws");

// Example radio data (this would be dynamically updated in a real scenario)
String message = "Nothing Yet";


// Function to send radio data to all connected WebSocket clients
void notifyClients() {
    const uint8_t size = JSON_OBJECT_SIZE(1);
    StaticJsonDocument<size> json;
    json["message"] = message;

    char data[28];
    size_t len = serializeJson(json, data);
    ws.textAll(data, len);
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
  Serial.begin(115200);
  radio.begin();
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
  char* receivedPacket = radio.readRadio(); // Call function to get received data
  
  if (receivedPacket) { // Check if a packet was received
      Serial.print("Processed Packet: ");
      Serial.println(receivedPacket);

      message = receivedPacket;
      // Notify WebSocket clients with the updated data
      notifyClients();

      // Free the dynamically allocated memory
      delete[] receivedPacket;
  }
    
  delay(1000); // Just a delay to simulate periodic checking
}
