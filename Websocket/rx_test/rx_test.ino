#include "radio_class.h"
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>
#include <ArduinoJson.h>
#include "LedController.hpp"

LedController<1,1> lc;

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
    switch (type) {
        case WS_EVT_CONNECT:
            Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
            break;
        case WS_EVT_DISCONNECT:
            Serial.printf("WebSocket client #%u disconnected\n", client->id());
            break;
        case WS_EVT_PONG:
        case WS_EVT_ERROR:
            break;
    }
}

void displayFloat(float value, unsigned int row = 0, unsigned int decimalPlaces = 1,unsigned int digitOffset = 0){
  unsigned int total_length = NUMBER_OF_DIGITS;
  if(NUMBER_OF_DIGITS<decimalPlaces){return;};

  if(value < 0){
    control.setChar(row,total_length-1+digitOffset,'-',false);
    total_length--;
  };

  for(unsigned int i = 0; i < decimalPlaces; i ++){
    value*=10.0f;
  }

  unsigned int v = (unsigned int) (value < 0 ? -value : value);

  for (unsigned int i = 0; i < total_length;i++){
    control.setDigit(row,i+digitOffset,v%10,i == decimalPlaces);
    v/=10;
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

  lc=LedController<1,1>(27,25,26);
  lc.setIntensity(8); /* Set the brightness to a medium values */
  lc.clearMatrix(); /* and clear the display */
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
