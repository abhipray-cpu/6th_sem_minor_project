//importing the required libraries
#include <WiFi.h>
#include <FirebaseESP32.h>
#include "time.h"
//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"
#define WIFI_SSID "fill the ssid of the wifi"
#define WIFI_PASSWORD "password of the wifi network"
#define FIREBASE_AUTH "wSpui4ViNhkKSdAToACWwwXw1PcgkbtAzwFstHL6"
#define FIREBASE_HOST "minor-project-d80d2-default-rtdb.asia-southeast1.firebasedatabase.app/"
FirebaseData firebaseData;
FirebaseJson json;
FirebaseData fbdo;
const int sense_pin0=34;
const int sense_pin1=32;


int read_value0 =0;
//int read_value1 =0;


void setup() {
  Serial.begin(115200); 
  delay(1000);
  WiFi.begin(WIFI_SSID,WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
   Serial.println();
   Serial.print("Connected with IP: ");
   Serial.println(WiFi.localIP());
   Serial.println(); 
   Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
   delay(700);
   Serial.println("Touch test");
}

void loop() {
  read_value0=analogRead(sense_pin0);
  if(Firebase.setFloat(fbdo, F("/pressure/value"),read_value0))
     {
      Serial.println("Updated pressure value successfully");
      Serial.print(read_value0);
      }
      else
      {
        Serial.println("Failed to update data");
        Serial.println(fbdo.errorReason().c_str());
        }
  
  delay(2000);
}
