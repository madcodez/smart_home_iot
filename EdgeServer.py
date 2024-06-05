
import json
import time
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883
WAIT_TIME = 0.25
REGISTER_DEVICE = "device/register"
REGISTER_STATUS = "register/status/"
DEVICE_STATUS = "device/status/"
DEVICE = "device/"
DEVICE_REGISTER_STATUS_MSG = "register/status/msg"


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
        self.client.subscribe(DEVICE_STATUS)
        self.client.subscribe(DEVICE_REGISTER_STATUS_MSG)

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
        if (msg.topic == DEVICE_REGISTER_STATUS_MSG):
            device = json.loads(msg.payload.decode())
            print(
                f"{device['msg']} Registered! - Registration status is available for {device['device_id']} : {device['flag']}\n")
        if (msg.topic == DEVICE_STATUS):

            device = json.loads(msg.payload.decode())
            print(
                f"Here is the current device-status for {device['device_id']} : {device}\n")

    # Returning the current registered list

    def get_registered_device_list(self):

        return self._registered_list

    # Getting the status for the connected devices
    def get_status_all(self):
        self.client.publish(DEVICE_STATUS + "all")

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

    def set_switch_status_id(self, device, payload):

        if device != None:
            if device._device_type == 'LIGHT':

                self.client.publish(DEVICE+str(device._device_id),
                                    json.dumps(payload))
            elif device._device_type == 'AC':

                self.client.publish(DEVICE+str(device._device_id),
                                    json.dumps(payload))

    def set_switch_status_device_type(self, device_type, payload):

        if device_type != None:
            if device_type == 'LIGHT':

                self.client.publish(DEVICE+device_type,
                                    json.dumps(payload))
            elif device_type == 'AC':
                self.client.publish(DEVICE+device_type,
                                    json.dumps(payload))

    # def set_switch_status_room_type(self, room_type, payload):
    #     self.client.publish(DEVICE+room_type,
    #                         json.dumps(payload))

    def set_switch_status_room_type(self, room_type, payload):
        room_devices = self.get_device_types_by_room_type(
            self._registered_list, room_type)

        for device in room_devices:

            if device['device_type'] == 'LIGHT':

                self.client.publish(DEVICE+room_type+"/light/" + str(device['device_id']),
                                    json.dumps(payload))
            else:
                self.client.publish(DEVICE+room_type+"/ac/" + str(device['device_id']),
                                    json.dumps(payload))

    def set_switch_status_all(self, payload):
        self.client.publish(DEVICE, json.dumps(payload))

    def get_device_types_by_room_type(self, list_of_devices, room_type):

        return [device for device in list_of_devices if device.get("room_type") == room_type]
