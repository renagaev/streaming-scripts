#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>


const char* ssid = "TP-Link_BE4E";
const char* password = "church088";

#define LISTEN_PORT 80

WiFiServer server(LISTEN_PORT);

void setup(void) {
  pinMode(16, OUTPUT);
  pinMode(5, OUTPUT);
  digitalWrite(16, HIGH);
  digitalWrite(5, HIGH);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  bool low = true;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    if(low){
      digitalWrite(16, LOW);

    }
    else{
      digitalWrite(16, HIGH);
      }
    low = !low;
    Serial.print(".");
  }
  digitalWrite(16, LOW);
  digitalWrite(5, LOW);
  Serial.println("");
  Serial.println("WiFi connected");

  server.begin();
  Serial.println("Server started");
  Serial.println(WiFi.localIP());
}
const char RED_ON = '1';
const char RED_OFF = '0';
const char GREEN_ON = '3';
const char GREEN_OFF = '2';
void loop() {

  WiFiClient client = server.available();

  if (client) {

    while (client.connected()) {

      while (client.available()>0) {
        char c = client.read();
        switch(c){
          case RED_ON:
            digitalWrite(16,HIGH);
            break;
          case RED_OFF:
            digitalWrite(16,LOW);
            break;
          case GREEN_ON:
            digitalWrite(5,HIGH);
            break;
          case GREEN_OFF:
            digitalWrite(5,LOW);
            break;
          default:
            break;
          }
      }

      delay(10);
    }

    client.stop();
  }
  delay(10);
}