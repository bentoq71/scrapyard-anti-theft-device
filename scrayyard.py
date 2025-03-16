from machine import Pin, PWM, time_pulse_us
import utime  

# Define properties
Properties = [
    {"Max_Distance": 10},
    {"Pulse_Timing": 10},
    {"Echo_PulseD": 1000}
]

trig_pin = Pin(15, Pin.OUT)
echo_pin = Pin(14, Pin.IN, Pin.PULL_DOWN) 

buzzer_pin = Pin(16, Pin.OUT)
buzzer = PWM(buzzer_pin)
buzzer.freq(1000)
buzzer.duty_u16(0)

def measure_distance():
    """Measure distance using HC-SR04 ultrasonic sensor."""
    trig_pin.low()
    utime.sleep_us(2)

    trig_pin.high()
    utime.sleep_us(Properties[1]["Pulse_Timing"])
    trig_pin.low()

    duration = time_pulse_us(echo_pin, 1, Properties[2]["Echo_PulseD"])

    if duration < 0:
        return None  

    distance = (duration / 2) / 29.1
    return distance

def main():
    while True:
        distance = measure_distance()

        if distance is not None:
            print("Distance: {:.2f} cm".format(distance))

            if distance >= Properties[0]["Max_Distance"]:
                buzzer.duty_u16(32768)
            else:
                buzzer.duty_u16(0)
        else:
            print("Out of range or no object detected.")
            buzzer.duty_u16(32768)

        utime.sleep(0.35)

# Run the program
main()
