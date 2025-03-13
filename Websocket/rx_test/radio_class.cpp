#include "radio_class.h"
#include <algorithm>

void Radio::init(){
    //init both un-encoded and encoded packet with 0
    std::fill_n(packet, packetSize, 0.0000);
    // std::fill_n(encodedPacket, packetSize * 4, '0');
}

// void Radio::led_test(Led *statusLed){
//   this->statusLed = statusLed;
//   statusLed->RGB2(0, 100, 0, 0);
//   statusLed->RGB2(1, 100, 100, 0);
  
// }

void Radio::begin(){
  pinMode(RFM69_RST, OUTPUT);
  digitalWrite(RFM69_RST, LOW);

  Serial.println("Feather RFM69 TX Test!");
  Serial.println();

  // manual reset
  digitalWrite(RFM69_RST, HIGH);
  delay(10);
  digitalWrite(RFM69_RST, LOW);
  delay(10);

  if (!rf69.init()) {
    Serial.println("RFM69 radio init failed");
    while (1);
  }
  Serial.println("RFM69 radio init OK!");
  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM (for low power module)
  // No encryption
  if (!rf69.setFrequency(RF69_FREQ)) {
    Serial.println("setFrequency failed");
  }

  // If you are using a high power RF69 eg RFM69HW, you *must* set a Tx power with the
  // ishighpowermodule flag set like this:
  rf69.setTxPower(20, true);  // range from 14-20 for power, 2nd arg must be true for 69HCW

  // // The encryption key has to be the same as the one in the server
  // uint8_t key[] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
  //                   0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
  // rf69.setEncryptionKey(key);

  Serial.print("RFM69 radio @");  Serial.print((int)RF69_FREQ);  Serial.println(" MHz");
}

// void Radio::begin(){

//     //radio stuff
//     pinMode(RFM69_RST, OUTPUT);
//     digitalWrite(RFM69_RST, HIGH);
    
//     // manual reset
//     digitalWrite(RFM69_RST, LOW);
//     delay(10);
//     digitalWrite(RFM69_RST, HIGH);
//     delay(10);

//     Serial.println("Hello!");

//     while (!rf69.init())
//     {
//         Serial.println("RF69 init failed");
//         // statusLed->RGB2(0, 255, 0, 0);
//         while (1)
//             ;
//     }
//     Serial.println("RF69 init OK!");
//     // statusLed->RGB2(0, 0, 0, 255);

//     // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
//     if (!rf69.setFrequency(RF69_FREQ))
//     {
//         Serial.println("setFrequency failed");
//         while (1)
//             ;
//     }
//     Serial.print("Set Freq to: ");
//     Serial.println(RF69_FREQ);

//     // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on
//     // attempt to speed up radio with Bw = 500 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on. Fast+short range
//     //rf95.setModemConfig(1);
//     // The default transmitter power is 13dBm, using PA_BOOST.
//     // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
//     // you can set transmitter powers from 5 to 23 dBm:
//     // rf95.setTxPower(13, false);
//     rf69.setTxPower(20, true);



//      delay(10);
//     //initalize EAST serial communication
//     // Serial8.begin(800000);  //east uses 8, prism uses 5
//     // EAST_serial.begin(Serial8);
// }

// union Radio::floatunion_t
// {
//     float f;
//     char a[sizeof(float)];
// } float_ur;

// float Radio::decoder(char *encoded)
// {
//     // Serial.println("Debug Decoder");
//     for (int i = 0; i < sizeof(float); i++)
//     {
//         float_ur.a[i] = encoded[i];
//         // Serial.println(encoded[i]);
//     }
//     return float_ur.f;
// }

// void Radio::sendingPacket()
// {
//     readSerial();

// }

//  char Radio::readSerial()
//  {
// //     // if (EAST_serial.available()){
// //     //   if(!serial_status){
// //     //     statusLed->RGB2(0, 0, 255, 0);
// //     //     serial_status = true;
// //     //   }
        
// // // //        Serial.println("Serial Data:");  
// // //         EAST_serial.rxObj(serialBuffer);
// // //         Serial.println(sizeof(serialBuffer));
// // //         sendRadio(serialBuffer);

        
// // //        if (sizeof(serialBuffer) != packetSize * 4)
// // //        {
// // //            Serial.println("Serial read length mismatch");
// // //        }
// //     }
// // //    else if(!EAST_serial.available())
// // //    {
// // //      Serial.println("not available");
// // //    }
// // //    return serialBuffer;
    

//  }

// void Radio::reveicePacket()
// {
//     if (rf95.available())
//     {
//         readRadio();
//         decodeData();
//         printData();
        
//     }
// }

void Radio::sendRadio(char *packet){
  
//    Serial.println(serialBuffer);
    // Send a message to rf95_server
  // if(data->validpacket)
  // {
  //   rf95.waitPacketSent();
  //   rf95.send((uint8_t *)data->encodedpacket, sizeof(data->encodedpacket));
  //   data->validpacket=false;
  // }
  Serial.print("Sending "); Serial.println(packet);
  rf69.send((uint8_t *)packet, strlen(packet));
  rf69.waitPacketSent();
//    delay(10);
//    rf95.waitPacketSent();
//    Serial.println("Packet Sent");
}

char* Radio::readRadio() {
    if (rf69.available()) {
        // Should be a message for us now
        uint8_t buf[RH_RF69_MAX_MESSAGE_LEN];
        uint8_t len = sizeof(buf);
        if (rf69.recv(buf, &len)) {
            if (!len) return nullptr;
            
            buf[len] = 0; // Null-terminate the buffer

            // Allocate memory for the packet
            char* receivedPacket = new char[len + 1]; // +1 for null terminator
            strcpy(receivedPacket, (char*)buf);

            // Serial.print("Received [");
            // Serial.print(len);
            // Serial.print("]: ");
            // Serial.println(receivedPacket);
            // Serial.print("RSSI: ");
            // Serial.println(rf69.lastRssi(), DEC);

            if (strstr(receivedPacket, "Hello World")) {
                // Send a reply!
                uint8_t data[] = "And hello back to you";
                rf69.send(data, sizeof(data));
                rf69.waitPacketSent();
                Serial.println("Sent a reply");
            }

            return receivedPacket; // Caller is responsible for freeing memory
        } else {
            Serial.println("Receive failed");
        }
    }
    return nullptr; // Return nullptr if no packet is received
}


// void Radio::readRadio()
// {
//     // Should be a message for us now
//     uint8_t serialBuffer[200]; // RH_RF95_MAX_MESSAGE_LEN
//     uint8_t len = sizeof(serialBuffer);

//     if (rf95.recv(serialBuffer, &len))
//     {
//         // RH_RF95::printserialBufferfer("Received: ", serialBuffer, len);
//         Serial.print("Got: ");
//         Serial.println((char *)serialBuffer);
//         Serial.print("RSSI: ");
//         Serial.println(rf95.lastRssi(), DEC);
//     }
//     else
//     {
//         Serial.println("Receive failed");
//     }
//     for (int i = 0; i < packetSize * 4; i++)
//     {
//         //      Serial.println((char)serialBuffer[i]);
//         encodedPacket[i] = (char)serialBuffer[i];
//     }
// }

// void Radio::decodeData()
// {
//     if (sizeof(encodedPacket) / sizeof(encodedPacket[0]) == packetSize * sizeof(float))
//     {
//         for (int i = 0; i < packetSize; i++)
//         {
//             char subencodedPacket[sizeof(float)];
//             for (int j = 0; j < sizeof(float); j++)
//             {
//                 subencodedPacket[j] = encodedPacket[i * sizeof(float) + j];
//             }
//             packet[i] = decoder(subencodedPacket);
//         }
//     }
// }

void Radio::printData()
{
    for (int k = 0; k < packetSize; k++)
    {
        Serial.print(packet[k]);
        Serial.print(",");
    }
    Serial.println();
};
