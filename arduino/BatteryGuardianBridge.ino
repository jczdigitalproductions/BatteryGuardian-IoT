#include <Arduino_RouterBridge.h>

// Demo-only alert indicator. Built-in LED assumed active-low; verify on board.
// Safety-critical battery protection MUST be implemented independently.
volatile int requestedLevel = 0;
unsigned long lastUpdateMs = 0;
const unsigned long timeoutMs = 5000;

void set_alert_level(int level) {
  if (level < 0 || level > 2) return;
  requestedLevel = level;
  lastUpdateMs = millis();
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  if (!Bridge.begin()) { while (true) { delay(100); } }
  Bridge.provide_safe("set_alert_level", set_alert_level);
}

void loop() {
  // Single built-in LED: off=normal; slow blink=warning; fast blink=critical.
  // Loss of updates produces a distinct fast blink (communications fault).
  int level = requestedLevel;
  if (millis() - lastUpdateMs > timeoutMs) level = 3;
  unsigned long period = (level == 1) ? 1000 : (level == 2 ? 250 : 125);
  bool on = (level != 0) && ((millis() / period) % 2 == 0);
  digitalWrite(LED_BUILTIN, on ? LOW : HIGH);
  delay(20);
}
