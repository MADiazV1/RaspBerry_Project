from flask import Flask, render_template, request, redirect, url_for
import paho.mqtt.client as mqtt

app = Flask(__name__)

mqttBroker = "192.168.67.91"
client = mqtt.Client("Flask_App")
client.connect(mqttBroker)

sensor_data = {"distance": "No data"}

def on_message(client, userdata, msg):
    global sensor_data
    sensor_data["distance"] = msg.payload.decode()
    print(f"Received message: {sensor_data['distance']}")

client.on_message = on_message
client.subscribe("sensor/ultrasonic")
client.loop_start()

@app.route('/')
def index():
    return render_template('index.html', data=sensor_data)

@app.route('/control', methods=['POST'])
def control():
    if request.method == 'POST':
        client.publish("control/gpio", "ON")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
