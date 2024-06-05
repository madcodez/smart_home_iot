import json
import paho.mqtt.client as mqtt
import time

HOST = "localhost"
PORT = 1883
REGISTER_DEVICE = "device/register"
REGISTER_STATUS = "register/status/"
DEVICE_REGISTER_STATUS_MSG = "register/status/msg"
DEVICE_STATUS = "device/status/"
DEVICE = "device/"


class Light_Device():

    # setting up the intensity choices for Smart Light Bulb
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]

    def __init__(self, device_id, room):
        # Assigning device level information for each of the devices.
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = "LIGHT"
        self._switch_status = "OFF"
        self.client = mqtt.Client(self._device_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._register_device(
            self._device_id, self._room_type, self._device_type)

    def _register_device(self, device_id, room_type, device_type):

        light_device = dict()
        light_device['device_id'] = device_id
        light_device['room_type'] = room_type
        light_device['device_type'] = device_type
        self.client.publish(REGISTER_DEVICE, json.dumps(light_device))

    # Connect method to subscribe to various topics.
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    def _on_connect(self, client, userdata, flags, result_code):

        self.client.subscribe(REGISTER_STATUS + str(self._device_id))
        self.client.subscribe(DEVICE_STATUS + str(self._device_id))
        self.client.subscribe(DEVICE_STATUS + str(self._device_type))
        self.client.subscribe(DEVICE_STATUS + str(self._room_type))
        self.client.subscribe(DEVICE_STATUS+"all")

        self.client.subscribe(DEVICE + str(self._device_id))
        self.client.subscribe(DEVICE + str(self._device_type))
        self.client.subscribe(
            DEVICE + str(self._room_type)+"/light/" + str(self._device_id))
        self.client.subscribe(DEVICE)
    # method to process the recieved messages and publish them on relevant topics
    # this method can also be used to take the action based on received commands

    def _on_message(self, client, userdata, msg):

        if msg.topic == REGISTER_STATUS + str(self._device_id):
            payload = {'msg': "LIGHT_DEVICE",
                       'device_id': self._device_id, 'flag': True}
            self.client.publish(
                DEVICE_REGISTER_STATUS_MSG, json.dumps(payload))

        if msg.topic == DEVICE_STATUS + str(self._device_id):
            self._get_status()
        if msg.topic == DEVICE_STATUS + str(self._device_type):
            self._get_status()
        if msg.topic == DEVICE_STATUS + str(self._room_type):
            self._get_status()
        if msg.topic == DEVICE_STATUS + "all":
            self._get_status()

        if msg.topic == DEVICE + str(self._device_id):
            payload = msg.payload.decode()
            status = json.loads(payload)
            self._set_status(status)

        if msg.topic == DEVICE + str(self._device_type):
            payload = msg.payload.decode()
            status = json.loads(payload)
            self._set_status(status)

        if msg.topic == DEVICE + str(self._room_type)+"/light/" + str(self._device_id):
            payload = msg.payload.decode()
            status = json.loads(payload)
            self._set_status(status)

        if msg.topic == DEVICE:
            payload = msg.payload.decode()
            status = json.loads(payload)
            self._set_status(status)
    # Getting the current switch status of devices

    def _get_status(self):
        device = {}
        device['device_id'] = self._device_id
        device['switch_status'] = self._get_switch_status()
        device['intensity'] = self._get_light_intensity()
        self.client.publish(
            DEVICE_STATUS, json.dumps(device))

    def _set_status(self, status):
        if (status.get('switch_status') is not None):
            self._set_switch_status(status['switch_status'])
        if (status.get('intensity') is None):
            self._set_light_intensity(self._light_intensity)
        elif (status.get('intensity') is not None and status.get('intensity') in self._INTENSITY):
            self._set_light_intensity(status['intensity'])
        else:
            print("Intensity Change FAILED. Invalid Light Intensity level received")
            pass
        self._get_status()

    def _get_switch_status(self):
        return self._switch_status
    # Setting the the switch of devices

    def _set_switch_status(self, switch_state=None):
        # if (self._switch_status != switch_state):
        if (switch_state is None):
            switch_state = self._switch_status
        if (self._switch_status != switch_state):
            self._switch_status = switch_state

        pass
    # Getting the light intensity for the devices

    def _get_light_intensity(self):
        return self._light_intensity

    # Setting the light intensity for devices

    def _set_light_intensity(self, light_intensity):
        if (self._light_intensity != light_intensity):
            self._light_intensity = light_intensity

    def _on_disconnect(self):
        pass
