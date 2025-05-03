#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>
#include <ArduinoJson.h>

// Replace with your network credentials
const char* ssid = "WS_server_test";

// Create an AsyncWebServer object on port 80
AsyncWebServer server(80);
// Create a WebSocket object on the path "/ws"
AsyncWebSocket ws("/ws");

// Example radio data (this would be dynamically updated in a real scenario)
int msg_number = 0;
int phase = 0;
unsigned long lastPhaseUpdate = 0; // Tracks the last time `phase` was updated
const unsigned long phaseUpdateInterval = 1000; // Delay in milliseconds (1 second)

// Function to send radio data to all connected WebSocket clients
void notifyClients() {
  const uint8_t size = JSON_OBJECT_SIZE(1);
  StaticJsonDocument<size> json;
  msg_number++;

  // Update `phase` only if the interval has passed
  unsigned long currentMillis = millis();
  if (currentMillis - lastPhaseUpdate >= phaseUpdateInterval) {
    phase++;
    if (phase > 5) {
      phase = 1;
    }
    lastPhaseUpdate = currentMillis;
  }
  //int mock_data = random(0, 100);
  json["time"] = msg_number;//dataBuffer[0];
  json["Accel_X"] = random(0, 100);//dataBuffer[1];
  json["Accel_Y"] = random(0, 100);//dataBuffer[2];
  json["Accel_Z"] = random(0, 100);//dataBuffer[3];
  json["Gyro_X"] = random(0, 100);
  json["Gyro_Y"] = random(0, 100);
  json["Gyro_Z"] = random(0, 100);
  json["Temp"] = random(0, 100);
  json["Euler_X"] = random(0, 100);
  json["Euler_Y"] = random(0, 100);
  json["Euler_Z"] = random(0, 100);
  json["Baro_Alt"] = random(0, 100);
  json["Longitude"] = random(0, 100);
  json["Latitude"] = random(0, 100);
  json["GPS_Alt"] = random(0, 100);
  json["Phase"] = phase;
  json["Continuity"] = random(0, 100);
  json["Voltage"] = random(0, 100);
  json["Link_Strength"] = random(0, 100);
  json["KF_X"] = random(0, 100);
  json["KF_Y"] = random(0, 100);
  json["KF_Z"] = random(0, 100);
  json["KF_VX"] = random(0, 100);
  json["KF_VY"] = random(0, 100);
  json["KF_VZ"] = random(0, 100);
  json["KF_Drag"] = random(0, 100);
  json["Diagnostic_Message"] = pow(2,2); // should trigger GPS error


  char data[512];
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

  // Notify WebSocket clients with the updated data
  notifyClients();
}