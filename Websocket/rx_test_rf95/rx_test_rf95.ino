#include "radio_class.h"
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>
#include <ArduinoJson.h>
#include "LedController.hpp"

LedController<1,1> lc;


Radio radio;
char radioPacket[112];
float dataBuffer[28];

const char* ssid = "WS_test";

// Create an AsyncWebServer object on port 80
AsyncWebServer server(80);
// Create a WebSocket object on the path "/ws"
AsyncWebSocket ws("/ws");

// Example radio data (this would be dynamically updated in a real scenario)
int message = 0;


// Function to send radio data to all connected WebSocket clients
void notifyClients() {
    const uint8_t size = JSON_OBJECT_SIZE(1);
    StaticJsonDocument<size> json;
    json["time"] = rand();//dataBuffer[0];
    json["Accel_X"] = rand();//dataBuffer[1];
    json["Accel_Y"] = rand();//dataBuffer[2];
    json["Accel_Z"] = rand();//dataBuffer[3];
    json["Gyro_X"] = dataBuffer[4];
    json["Gyro_Y"] = dataBuffer[5];
    json["Gyro_Z"] = dataBuffer[6];
    json["Temp"] = dataBuffer[7];
    json["Euler_X"] = dataBuffer[8];
    json["Euler_Y"] = dataBuffer[9];
    json["Euler_Z"] = dataBuffer[10];
    json["Baro_Alt"] = dataBuffer[11];
    json["Longitude"] = dataBuffer[12];
    json["Latitude"] = dataBuffer[13];
    json["GPS_Alt"] = dataBuffer[14];
    json["Phase"] = dataBuffer[15];
    json["Continuity"] = dataBuffer[16];
    json["Voltage"] = dataBuffer[17];
    json["Link_Strength"] = dataBuffer[18];
    json["KF_X"] = dataBuffer[19];
    json["KF_Y"] = dataBuffer[20];
    json["KF_Z"] = dataBuffer[21];
    json["KF_VX"] = dataBuffer[22];
    json["KF_VY"] = dataBuffer[23];
    json["KF_VZ"] = dataBuffer[24];
    json["KF_Drag"] = dataBuffer[25];
    json["Diagnostic_Message"] = dataBuffer[27];


    char data[512];
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
  unsigned int total_length = 4;
  if(4<decimalPlaces){return;};

  if(value < 0){
    lc.setChar(row,total_length-1+digitOffset,'-',false);
    total_length--;
  };

  for(unsigned int i = 0; i < decimalPlaces; i ++){
    value*=10.0f;
  }

  unsigned int v = (unsigned int) (value < 0 ? -value : value);

  for (unsigned int i = 0; i < total_length;i++){
    lc.setDigit(row,i+digitOffset,v%10,i == decimalPlaces);
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
  radio.receivePacket();

  // float dataBuffer[28];
  radio.getData(&dataBuffer[0]);
  for (int i = 0; i<28; i++) {
    Serial.print(dataBuffer[i]);
    Serial.print(", ");
  }
  Serial.print("\n");
  // if (radio.readRadio(radioPacket, sizeof(radioPacket))) {
  //     Serial.print("Final received data: ");
  //     Serial.println(radioPacket);
  //     message = radioPacket;
  //     // Notify WebSocket clients with the updated data
  //     notifyClients();
  int RSSI = radio.getRSSI();
  Serial.print("RSSI: ");
  Serial.println(RSSI);
  displayFloat(RSSI);
  // }
  notifyClients();

  delay(200); // Just a delay to make sure WS doesn't get overwhelmed
}
