import time
import board
import math
import audiopwmio
import audiocore
import pwmio
from adafruit_circuitplayground import cp
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

motor = pwmio.PWMOut(pin=board.A2, duty_cycle=0, frequency=1000)

ble = BLERadio()
ble.name = "Nandini"
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

THRESHOLD = 5
step_count = 0
last_acceleration = cp.acceleration  # Initialize last_acceleration

def detect_steps():
    global step_count, last_acceleration  # Declare global variables
    current_acceleration = cp.acceleration

    # Calculate the magnitude of acceleration change
    acceleration_change = abs(current_acceleration.x - last_acceleration.x) + \
                           abs(current_acceleration.y - last_acceleration.y) + \
                           abs(current_acceleration.z - last_acceleration.z)

    # Check if acceleration change exceeds a threshold
    if acceleration_change > THRESHOLD:
        step_count += 1

    # Update last_acceleration for the next iteration
    last_acceleration = current_acceleration

    return step_count


def set_timer(time_str):
    words = time_str.split()
    for i, word in enumerate(words):
        if word.lower() == "timer":
            for j in range(i + 1, len(words)):
                if words[j][:-1].isdigit():
                    value = int(words[j][:-1])
                    unit = words[j][-1].lower()
                    if unit == "s":
                        duration = value
                    elif unit == "m":
                        duration = value * 60
                    elif unit == "h":
                        duration = value * 3600
                    print("Setting timer for", duration, "seconds")
                    time.sleep(duration)
                    print("Timer finished")
                    for i in range(3):
                        cp.play_file("dip.wav")
                        motor.duty_cycle = 32768
                        time.sleep(0.1)
                        motor.duty_cycle = 0
                        time.sleep(0.3)
                    return

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    ble.stop_advertising()
    print("Connected!")

    while ble.connected:
        if cp.button_a:
            cp.pixels[0] = (0, 255, 0) # LED's 0 and 1 shine into your finger
            cp.pixels[1] = (0, 255, 0)
            NUM_OVERSAMPLE = 10 # How many light readings per sample
            NUM_SAMPLES = 20 # How many samples we take to calculate 'average'
            samples = [0] * NUM_SAMPLES
            while True:
                if cp.button_b:
                    cp.pixels[0] = (0, 0, 0)
                    cp.pixels[1] = (0, 0, 0)
                    cp.pixels[9] = (0, 0, 0)
                    break
                for i in range(NUM_SAMPLES):
                    oversample = 0
                    for s in range(NUM_OVERSAMPLE):
                        oversample += float(cp.light)
                    samples[i] = oversample / NUM_OVERSAMPLE
                    mean = sum(samples) / float(len(samples))
                    print((samples[i] - mean,))
                        # Pulse LED #9 when sign changes
                    if i > 0:
                        if (samples[i]-mean) <= 0 and (samples[i-1]-mean) > 0:
                            cp.pixels[9] = (20, 0, 0)
                        else:
                            cp.pixels[9] = (0, 0, 0)
                    time.sleep(0.025)

        # Check if button B is pressed
        if cp.button_b:
            # Clear LEDs and exit the loop
            cp.pixels[0] = (0, 0, 0)
            cp.pixels[1] = (0, 0, 0)
            cp.pixels[9] = (0, 0, 0)

        if uart_server.in_waiting:
            received_string = uart_server.readline().strip().decode("utf-8")
            print("Received:", received_string)
            if "timer" in received_string.lower():
                set_timer(received_string)

        # Read temperature
        temperature_c = cp.temperature

        # Send temperature over UART
        uart_server.write("Temperature: {:.2f} C\n".format(temperature_c).encode("utf-8"))

        # Detect steps
        steps = detect_steps()
        #print("Steps:", steps)  # Send steps over serial console
        uart_server.write("Steps: {}\n".format(steps).encode("utf-8"))
        print(steps)
        time.sleep(0.1)