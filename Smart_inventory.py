#include <AccelStepper.h>
#include <NewPing.h>

// Pin Definitions
#define TRIGGER_PIN 9
#define ECHO_PIN 10
#define MAX_DISTANCE 30  // in cm

#define MOTOR_STEP_PIN 2
#define MOTOR_DIR_PIN 3

#define BUTTON_NEXT 4
#define BUTTON_PREV 5

// Sensor and Stepper Setup
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
AccelStepper stepper(AccelStepper::DRIVER, MOTOR_STEP_PIN, MOTOR_DIR_PIN);

// Variables
int containerIndex = 0;
const char* containers[] = {"Rice", "Sugar", "Dal", "Salt"};
int containerSteps[] = {0, 200, 400, 600}; // Adjust based on your platform

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_NEXT, INPUT_PULLUP);
  pinMode(BUTTON_PREV, INPUT_PULLUP);

  stepper.setMaxSpeed(500);
  stepper.setAcceleration(200);

  displayContainer(containerIndex);
}

void loop() {
  if (!digitalRead(BUTTON_NEXT)) {
    containerIndex = (containerIndex + 1) % 4;
    rotateTo(containerSteps[containerIndex]);
    displayContainer(containerIndex);
    delay(300);
  }

  if (!digitalRead(BUTTON_PREV)) {
    containerIndex = (containerIndex - 1 + 4) % 4;
    rotateTo(containerSteps[containerIndex]);
    displayContainer(containerIndex);
    delay(300);
  }
}

void rotateTo(int stepTarget) {
  stepper.moveTo(stepTarget);
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }
}

void displayContainer(int index) {
  int distance = sonar.ping_cm();
  String level;

  if (distance == 0) level = "Empty";
  else if (distance < 5) level = "Full";
  else if (distance < 10) level = "Medium";
  else level = "Low";

  Serial.print("Container: ");
  Serial.println(containers[index]);
  Serial.print("Level: ");
  Serial.println(level);
  Serial.println("---------------------");
}
