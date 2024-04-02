#include <WiFi.h>
#include <WiFiUDP.h>

WiFiUDP udp;
char ssid[] = "MiniAvionics"; // defined the ssid as a global function whose value gets assigned in the setup() function
char clientAddress[] = "172.24.240.182"; // confirm we'll only have one (There is a constraint based on how many people can access WiFi on ESP32?)
//char clientAddress[] = "192.168.4.2"
unsigned int localUdpPort = 4210;
unsigned int MAX_SIZE = 168;
char message[28][6] = {}; // scaffholded message which I'll receive from Daniel code. 

// setup the WiFi connection once - this is maintained across function calls
void setup() {
  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); // wait for everything to be connected
  }
  udp.begin(localUdpPort);
}

// define the max char array and [6] defines max number of char/null terminator. This definition is helpful for the compiler to compute offsets in the array
void sendArrOverUDP(char message[][6]) {
  // TODO: need stopping condition for this
  while (true) {
    char serializedMessage[MAX_SIZE]; // This is an estimate based on # of strings (28) * (# of chars + 1 for null terminator)
    int offset = 0; // offset is used to know where in the string buffer we're writing to so nothing gets overwritten
    // we want to loop through the message which is an input and copy it? Where does the serialization happen?
    for (int i = 0; i < 28; i++) {
      strcpy(serializedMessage + offset, message[i]);
      offset += strlen(message[i]); // offset's position changes based on the length of the string so it knows where in the buffer to write next
      if (i < 27) {
        serializedMessage[offset] = ',';
        offset++; // increment offset by 1 because we've added delimiter
      }
    }
  }
  udp.beginPacket(clientAddress, localUdpPort);
  udp.write((const uint8_t *) serializedMessage, offset);
  udp.endPacket();
}

void loop() {
    sendArrOverUDP(message);
}