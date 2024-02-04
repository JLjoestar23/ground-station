/* Usage
 * run http://192.168.4.1 on the local web browser
*/

/* INCLUDE LIBRARIES */
#include <WiFi.h>
#include <WiFiUDP.h>
#include "SPIFFS.h"

WiFiUDP udp;
unsigned int localUdpPort = 4210;
char incomingPacket[255];
const char* ssid = "MiniAvionics";
const char* serverAddress = "192.168.4.1";

WiFiServer server(80);

void setup(){
  Serial.begin(115200);

  WiFi.softAP(ssid);  // Set up the access point
  udp.begin(localUdpPort);   // Start the server with a port to listen to
  
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.softAPIP().toString().c_str(), localUdpPort);

  // Check if the log file exists in the SPIFFS system on ESP32
  if (!SPIFFS.begin(true)) {
    Serial.println("An Error has occured while mounting");
  } else {
    Serial.println("SPIFFS mounted successfuly");
  }
  
  Serial.println(SPIFFS.exists("/4_21_2082_refactored.txt"));
}

void loop() {
  int packetSize = udp.parsePacket(); // parse the incoming packet size
  if (packetSize) {
    int len = udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = 0;
    }
    Serial.printf("Received packet of size %d from %s:%d\n    (Hex: %s)\n", packetSize, udp.remoteIP().toString().c_str(), udp.remotePort(), incomingPacket);
    
    File file = SPIFFS.open("/4_21_2082_refactored.txt");
    if (file) {
      while (file.available()) {
        char fileBuffer[128];
        size_t bytesRead = file.readBytes(fileBuffer, sizeof(fileBuffer));
        udp.beginPacket(udp.remoteIP(), udp.remotePort()); // prepares to start sending data over UDP
        udp.write((const uint8_t*)fileBuffer, bytesRead);
        udp.endPacket();
      }
      file.close();
    } else {
      Serial.println("Failed to open file for reading");
    }
}
}