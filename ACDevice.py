
import json
import paho.mqtt.client as mqtt


HOST = "localhost"
PORT = 1883

REGISTER_DEVICE = "device/register"
REGISTER_STATUS = "register/status/"
DEVICE_STATUS = "device/status/"
DEVICE = "device/"
DEVICE_REGISTER_STATUS_MSG = "register/status/msg"


class AC_Device():

    _MIN_TEMP = 18
    _MAX_TEMP = 32

    def __init__(self, device_id, room):

        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = "AC"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._register_device(
            self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    # calling registration method to register the device
    def _register_device(self, device_id, room_type, device_type):
        ac_device = dict()
        ac_device['device_id'] = device_id
        ac_device['room_type'] = room_type
        ac_device['device_type'] = device_type
        self.client.publish(REGISTER_DEVICE, json.dumps(ac_device))

    # Connect method to subscribe to various topics.
    def _on_connect(self, client, userdata, flags, result_code):
        self.client.subscribe(REGISTER_STATUS + str(self._device_id))
        self.client.subscribe(DEVICE_STATUS + str(self._device_id))
        self.client.subscribe(DEVICE_STATUS + str(self._device_type))
        self.client.subscribe(DEVICE_STATUS + str(self._room_type))
        self.client.subscribe(DEVICE_STATUS+"all")
        self.client.subscribe(DEVICE + str(self._device_id))
        self.client.subscribe(DEVICE+str(self._device_type))
        self.client.subscribe(
            DEVICE+str(self._room_type)+"/ac/" + str(self._device_id))
        self.client.subscribe(DEVICE)
    # method to process the recieved messages and publish them on relevant topics
    # this method can also be used to take the action based on received commands

    def _on_message(self, client, userdata, msg):
        if msg.topic == REGISTER_STATUS + str(self._device_id):
            payload = {'msg': "AC_DEVICE", 'device_id': self._device_id,
                       'flag': True}
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

        if msg.topic == DEVICE + str(self._room_type)+"/ac/" + str(self._device_id):
            payload = msg.payload.decode()
            status = json.loads(payload)
            self._set_status(status)

        if msg.topic == DEVICE:
            payload = msg.payload.decode()
            status = json.loads(payload)
            self._set_status(status)

    def _get_status(self):
        device = {}
        device['device_id'] = self._device_id
        device['switch_status'] = self._get_switch_status()
        device['temperature'] = self._get_temperature()
        self.client.publish(
            DEVICE_STATUS, json.dumps(device))

    def _set_status(self, status):
        if (status.get('switch_status') is not None):
            self._set_switch_status(status['switch_status'])
        if (status.get('temperature') is None):
            self._set_temperature(self._temperature)
        elif (status.get('temperature') is not None and status['temperature'] >= self._MIN_TEMP and status['temperature'] <= self._MAX_TEMP):
            self._set_temperature(status['temperature'])
        else:
            print("Temperature Change FAILED. Invalid temperature value received")
            pass
        self._get_status()

    def _get_switch_status(self):
        return self._switch_status
    # Setting the the switch of devices

    def _set_switch_status(self, switch_state=None):
        if (switch_state is None):
            switch_state = self._switch_status
        if (self._switch_status != switch_state):
            self._switch_status = switch_state

    # Getting the temperature for the devices

    def _get_temperature(self):
        return self._temperature

    # Setting up the temperature of the devices
    def _set_temperature(self, temperature):
        if (self._temperature != temperature):
            self._temperature = temperature

    def _on_disconnect(self):
        pass
