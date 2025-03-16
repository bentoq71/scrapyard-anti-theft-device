from machine import Pin, PWM, time_pulse_us
import utime  

# Define properties
Properties = [
    {"Max_Distance": 10},   # Max distance before buzzer activates
    {"Pulse_Timing": 10},    # Trigger pulse duration in µs
    {"Echo_PulseD": 1000}   # Echo timeout in µs (30ms)
]

# Define pins
trig_pin = Pin(15, Pin.OUT)
echo_pin = Pin(14, Pin.IN, Pin.PULL_DOWN)  # Added pull-down resistor for stability

# Define pin for the piezo buzzer
buzzer_pin = Pin(16, Pin.OUT)
buzzer = PWM(buzzer_pin)
buzzer.freq(1000)  # Set PWM frequency for the buzzer (e.g., 2000 Hz)
buzzer.duty_u16(0)  # Start with the buzzer off

def measure_distance():
    """Measure distance using HC-SR04 ultrasonic sensor."""
    # Ensure trigger is LOW
    trig_pin.low()
    utime.sleep_us(2)

    # Send a 10us pulse to trigger the sensor
    trig_pin.high()
    utime.sleep_us(Properties[1]["Pulse_Timing"])
    trig_pin.low()

    # Measure the duration of the echo pulse
    duration = time_pulse_us(echo_pin, 1, Properties[2]["Echo_PulseD"])

    # If timeout or no echo received
    if duration < 0:
        return None  

    # Convert time to distance in cm
    distance = (duration / 2) / 29.1  # Speed of sound = 343 m/s
    return distance

# Main loop
def main():
    while True:
        distance = measure_distance()

        if distance is not None:
            print("Distance: {:.2f} cm".format(distance))

            # Trigger the buzzer if an object is within Max_Distance
            if distance >= Properties[0]["Max_Distance"]:
                buzzer.duty_u16(32768)  # Turn on buzzer (50% duty cycle)
            else:
                buzzer.duty_u16(0)  # Turn off buzzer
        else:
            print("Out of range or no object detected.")
            buzzer.duty_u16(32768)

        utime.sleep(0.35)  # Wait 1 second before next reading

# Run the program
main()
