
// resources:
// https://randomnerdtutorials.com/esp32-useful-wi-fi-functions-arduino/

#include <WiFi.h>

// constants
const char *ssid = "TEST_SSID";
const char *password = "TEST_PASSWORD";
const int baudRate = 115200;

void setup()
{
    Serial.begin(baudRate);
    WiFi.mode(WIFI_AP);
    WiFi.softAP(ssid, password);

    Serial.println("\nConnecting to ground station");

    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(100);
    }

    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local ESP32 IP: ");
    Serial.println(WiFi.localIP());
}

void loop()
{
}