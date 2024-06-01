import RPi.GPIO as gp
import time
import paho.mqtt.client as mqtt

TRIG = 40
ECHO = 38
TRIG1 = 35
ECHO1 = 37
GPIO_PIN = 33

gp.setmode(gp.BOARD)
gp.setup(TRIG, gp.OUT)
gp.setup(ECHO, gp.IN)
gp.setup(TRIG1, gp.OUT)
gp.setup(ECHO1, gp.IN)
gp.setup(GPIO_PIN, gp.OUT)

mqttBroker = "192.168.67.91"
client = mqtt.Client("RaspberryPi")
client.connect(mqttBroker)

def ANCHO():
    gp.output(TRIG, True)
    time.sleep(0.00001)
    gp.output(TRIG, False)

    start_time = time.time()
    while gp.input(ECHO) == 0:
        start_time = time.time()
    end_time = time.time()

    while gp.input(ECHO) == 1:
        end_time = time.time()

    pulse = end_time - start_time
    distance = pulse * 34300 / 2
    return distance

def LARGO():
    gp.output(TRIG1, True)
    time.sleep(0.00001)
    gp.output(TRIG1, False)

    start_time = time.time()
    while gp.input(ECHO1) == 0:
        start_time = time.time()
    end_time = time.time()

    while gp.input(ECHO1) == 1:
        end_time = time.time()

    pulse = end_time - start_time
    distance = pulse * 34300 / 2
    return distance

def on_message(client, userdata, msg):
    if msg.topic == "control/gpio" and msg.payload.decode() == "ON":
        gp.output(GPIO_PIN, gp.HIGH)
        time.sleep(1)
        gp.output(GPIO_PIN, gp.LOW)
        print("GPIO 33 activado por 1 segundo")

client.on_message = on_message
client.subscribe("control/gpio")
client.loop_start()

try:
    while True:
        ancho = ANCHO()
        largo = LARGO()
        print("Ancho: ", ancho, " y largo: ", largo)
        area = ancho * largo
        print("Area:", str(area), "cm²")
        client.publish("sensor/ultrasonic", str(area))
        time.sleep(1)
except KeyboardInterrupt:
    gp.cleanup()
