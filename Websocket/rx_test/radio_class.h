#pragma once
// #include "led_class.h"
// #include <Arduino.h>
// #include <algorithm>
// #include <RH_RF95.h>
#include <RH_RF69.h>
// #include "data_class.h"

// #define RFM95_CS 5
// #define RFM95_RST 22
// #define RFM95_INT 4
// #define RF95_FREQ 434.0
#define RFM69_CS 5
#define RFM69_RST 22
#define RFM69_INT 4
#define RF69_FREQ 434.0

class Radio {
  private:
    RH_RF69 rf69;
    const static int packetSize = 28;
    // float packet[packetSize];
    char packet[packetSize];
    // char encodedPacket[packetSize*4];
    // union floatunion_t;
    // float decoder(char* encoded);
    // char serialBuffer[packetSize*4];
    // Led *statusLed;
    // bool serial_status;
    // Data *data;

    
    

  public:

//    Radio(Led *statusLed);
    // Radio(Data *data) : rf95(RFM95_CS,RFM95_INT) {this->data = data; init();} ;
    Radio() : rf69(RFM69_CS, RFM69_INT){};

    
    void init();  
    void begin(); 
    void reveicePacket();  
    // void led_test(Led *statusLed);
 
    void sendRadio(char *packet);
    //void sendRadio();
    char* readRadio();
    //void decodeData();  
    void printData();
    // void sendingPacket();
    // char readSerial();

};
