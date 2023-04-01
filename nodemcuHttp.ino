#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>


const char* ssid = "Church_Hall";
const char* password = "church088";

#define LISTEN_PORT 80

ESP8266WebServer server(LISTEN_PORT);

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
  server.on("/red_on", handleRedOn);
  server.on("/red_off", handleRedOff);
  server.on("/green_on", handleGreenOn);
  server.on("/green_off", handleGreenOff);
}
void handleRedOn() {
  digitalWrite(16,HIGH);
  server.send(200, "text/plain", "ok");
}
void handleRedOff() {
  digitalWrite(16,LOW);
  server.send(200, "text/plain", "ok");
}
void handleGreenOn() {
  digitalWrite(5,HIGH);
  server.send(200, "text/plain", "ok");
}
void handleGreenOff() {
  digitalWrite(5,LOW);
  server.send(200, "text/plain", "ok");
}

void loop(void){
  server.handleClient();
}
