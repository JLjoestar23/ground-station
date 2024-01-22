#include <FS.h>
#include "SPIFFS.h"

void setup() {
  Serial.begin(115200);

  if (!SPIFFS.begin(true)) {
    Serial.println("SPIFFS initialization failed!");
    return;
  }

  Serial.println("Total space: " + String(SPIFFS.totalBytes()));
  Serial.println("Used space: " + String(SPIFFS.usedBytes()));
  Serial.println("Free space: " + String(SPIFFS.totalBytes() - SPIFFS.usedBytes()));
}

void loop() {
  // Your main code here
}
