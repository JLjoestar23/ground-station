#include <WiFi.h>
#include <WiFiUDP.h>

WiFiUDP udp;
// char ssid[] = "OLIN"; // defined the ssid as a global function whose value gets assigned in the setup() function
const char* ssid = "OLIN-VISITOR"; // Did not work on OLIN private network - does work on public network
char serverAddress[] = "10.77.0.179"; // confirm we'll only have one (There is a constraint based on how many people can access WiFi on ESP32?)
//char clientAddress[] = "192.168.4.2"
unsigned int localUdpPort = 4210;
unsigned int MAX_SIZE = 168;

char message[27][6] = {
  "28", "29", "30", "42", "4002", "419", 
  "325", "328", "320", "123", "158", "160",
  "158", "158", "158", "158", "158", "158",
  "1925", "158", "158", "1582", "158", "158",
  "1258", "1058", "1538"
  };

// setup the WiFi connection once - this is maintained across function calls
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println(ssid); // For debugging purposes - know where it's connecting too
  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); // wait for everything to be connected
    Serial.print("Attempting to connect.");
    Serial.println(WiFi.status());
  } 
  // TODO: Check if the WiFi is actually connected
  // TODO: Confirm how we get from being connected to actually writing the packet
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi is connected");
  }
  udp.begin(localUdpPort);
}

// define the max char array and [6] defines max number of char/null terminator. This definition is helpful for the compiler to compute offsets in the array
void sendArrOverUDP(char message[][6]) {
  char serializedMessage[MAX_SIZE]; // This is an estimate based on # of strings (28) * (# of chars + 1 for null terminator)
  int offset = 0;
    // TODO: need stopping condition for this
    // we want to loop through the message which is an input and copy it? Where does the serialization happen?
  for (int i = 0; i < 28; i++) {
    strcpy(serializedMessage + offset, message[i]);
    offset += strlen(message[i]); // offset's position changes based on the length of the string so it knows where in the buffer to write next
    if (i < 27) {
      serializedMessage[offset] = ',';
      offset++; // increment offset by 1 because we've added delimiter
      }
    }
  udp.beginPacket(serverAddress, localUdpPort);
  udp.write((const uint8_t*)serializedMessage, offset);
  udp.endPacket(); // Returns 1 if the packet is sent successfully, 0 if otherwise (https://www.arduino.cc/reference/en/libraries/wifi/wifiudp.endpacket/)
  if (udp.endPacket() == 1) {
    Serial.println("Sent successfully...");
  } else {
    Serial.println("Sent unsuccessfully...");
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    sendArrOverUDP(message);
    delay(1000);
  }
}