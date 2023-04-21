
import json
import time
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883
WAIT_TIME = 0.25
REGISTER_DEVICE = "device/register"
REGISTER_STATUS = "register/status/"
DEVICE_STATUS = "device/status/"


class Edge_Server:

    def __init__(self, instance_name):

        self._instance_id = instance_name

        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._registered_list = []

    # Terminating the MQTT broker and stopping the execution

    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.
    def _on_connect(self, client, userdata, flags, result_code):
        self.client.subscribe(REGISTER_DEVICE)

    # method to process the recieved messages and publish them on relevant topics
    # this method can also be used to take the action based on received commands

    def _on_message(self, client, userdata, msg):
        if (msg.topic == REGISTER_DEVICE):
            payload = msg.payload.decode()
            device = json.loads(payload)

            print(
                f"Registration request is acknowledged for device {device['device_id']} in {device['room_type']}")
            print(f"Request is processed for {device['device_id']} .")
            flag = True
            self._registered_list.append(device)
            self.client.publish(
                REGISTER_STATUS + str(device['device_id']), json.dumps(flag))

    # Returning the current registered list

    def get_registered_device_list(self):

        return self._registered_list

    # Getting the status for the connected devices
    def get_status(self):
        self.client.publish(DEVICE_STATUS)

    def get_status_device_id(self, device_id):
        if device_id != None:
            self.client.publish(DEVICE_STATUS+str(device_id),
                                )

    def get_status_device_type(self, device_type):

        if device_type != None:
            self.client.publish(DEVICE_STATUS+str(device_type))

    def get_status_room_type(self, room_type):

        if room_type != None:
            self.client.publish(DEVICE_STATUS+str(room_type))
    # Controlling and performing the operations on the devices
    # based on the request received

    def set(self, device):
        pass
