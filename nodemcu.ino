#include <ESP8266WiFi.h>

#include <aREST.h>

aREST rest = aREST();

const char* ssid = "SSID";
const char* password = "PASSWORD";

#define LISTEN_PORT 80

WiFiServer server(LISTEN_PORT);

IPAddress ip(192, 168, 0, 113);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);
void setup(void) {
  Serial.begin(115200);

  rest.set_id("1");
  rest.set_name("esp8266");

  bool a = WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password);
  Serial.println(a);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  server.begin();
  Serial.println("Server started");

  Serial.println(WiFi.localIP());
}

void loop() {

  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  while (!client.available()) {
    delay(1);
  }
  rest.handle(client);

}
