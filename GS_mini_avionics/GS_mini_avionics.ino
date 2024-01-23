/* Usage
 * run http://192.168.4.1 on the local web browser
*/

/* INCLUDE LIBRARIES */
#include <WiFi.h>
#include "SPIFFS.h"

const char* ssid = "MiniAvionics";
// const char* wpa = "123456555";
const char* serverAddress = "http://192.168.4.1";

WiFiServer server(80);

void setup(){
  Serial.begin(115200);

  // Set up the access point
  WiFi.softAP(ssid);

  // Start the server
  server.begin();
  
  Serial.println("SoftAP started with IP: " + WiFi.softAPIP().toString());

  // Check if the log file exists in the SPIFFS
  if (!SPIFFS.begin(true)) {
    Serial.println("An Error has occured while mounting");
  } else {
    Serial.println("SPIFFS mounted successfuly");
  }
  
  Serial.println(SPIFFS.exists("/4_21_2082_refactored.txt"));
}

void loop(){
//   Check if a client has connected
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New client connected");

    // Open the file for reading
    File file = SPIFFS.open("/4_21_2082_refactored.txt"); // file path for the SPIFF doesn't include same structure as computer file path

    if (file) {
      //Read and print the content of the file
      while (file.available()) {
        Serial.print(char(file.read()));
      }

      file.close();
    } 

    else {
      Serial.println("Failed to open file");
    }
    
    client.stop();
    Serial.println("Client disconnected");
  } else {
    Serial.println("There is no client found.");
  }
}