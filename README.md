# Wearable System for Sensing and Feedback

The features of a wearable device depend on where the user will be wearing the device. For this project, I chose to design a wrist wearable device (essentially a watch). To begin with, I 3D printed Adafruit’s existing design for the [Circuit Playground](https://www.thingiverse.com/thing:1682293). The print was a little tight (and a little too compact), and in the interest of time, I changed the idea to a wearable glove!

## Features:

- **Bluetooth Connectivity:** like any other wearable watch, this device works once connected to your phone (through the Bluefruit app). I’m using UART protocol to communicate with the phone. Once connected, the interactions can be done both by receiving and sending data (explained below).
- **Step Counter:** I’m making use of a change in acceleration, measured by the built-in accelerometer in the Circuit Playground, to understand if the user is moving. Certain nuances concerned:
  - Sometimes, the user is just moving their hand and not necessarily taking a step; how does the algorithm handle this? By adding a threshold value (set by trial and error), the algorithm counts acceleration as a step only if it’s above the threshold, eliminating the possibility of tiny motions being counted as steps.
  - Will motion be considered in all 3 axes? Since there can be elevation while walking, I did not restrict the axis on which acceleration is considered. This could mean that jumps and other motions might be considered as steps. Incorporating the accelerometer with a GPS might help to measure steps more accurately.
- **Heartbeat Sensor:** By lighting up two neopixels to a bright green light, when the user places their finger on the light sensor, the light reflected gets a general idea of the heart rate. Using this, I blink the red LED on another neopixel to indicate the beating heart. This mode can be accessed by pressing Button A on the board. The user can exit the heartbeat sensor mode by pressing Button B.
- **Temperature Sensor:** Using the temperature sensor on the Circuit Playground, we can measure the ambient temperature in the room and the user’s body temperature (to some extent). This can be done by placing the finger on the sensor. I’m sending this data via UART to the Bluefruit App; it can be seen on the plotter and in the UART console.
- **Timer:** This feature incorporates taking input from the user. Once the user enters the text “timer XYZ” in the UART console on the Bluefruit app, they can set a timer on the Circuit Playground watch. Here, XYZ represents a numeric value and either s, m, or h to indicate seconds, minutes, or hours. For example, “timer 5s” sets a timer for 5 seconds. Once the timer ends, an audio file is played from the speaker, and the motor vibrates in a heartbeat pattern for a haptic effect.
