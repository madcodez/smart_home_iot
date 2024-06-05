import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 0.50
COMMAND_ID = 0
print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user
edge_server_1 = Edge_Server('edge_server_1')
time.sleep(WAIT_TIME)

# Creating the light_device
print("Intitate the device creation and registration process.")
print("\nCreating the Light devices for their respective rooms.")
light_publisher1 = Light_Device("light_1", "kitchen")
light_publisher2 = Light_Device("light_2", "bedroom")
light_publisher3 = Light_Device("light_3", "living_room")
ac_publisher1 = AC_Device("ac_1", "bedroom")
ac_publisher2 = AC_Device("ac_2", "living_room")


time.sleep(WAIT_TIME)


registered_devices = edge_server_1.get_registered_device_list()
device_ids = []
for device in registered_devices:
    device_ids.append(device['device_id'])
print('The Registered devices on Edge-Server:', device_ids)


print("\n******************* GETTING THE STATUS BY DEVICE_ID *******************\n\n")
for i in range(len(registered_devices)):

    COMMAND_ID = i + 1
    print(F"Command ID {COMMAND_ID} request is intiated.\n")
    time.sleep(WAIT_TIME)
    edge_server_1.get_status_device_id(registered_devices[i]['device_id'])
    time.sleep(WAIT_TIME)
    print(f"Command ID {COMMAND_ID} is executed.\n")


print("******************* GETTING THE STATUS BY DEVICE_TYPE *******************\n\n")
COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.get_status_device_type('LIGHT')
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.get_status_device_type('AC')
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

print("******************* GETTING THE STATUS BY ROOM_TYPE *******************\n\n")
COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.get_status_room_type('bedroom')
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

print("******************* GETTING THE STATUS BY ENTIRE_HOME *******************\n\n")
COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.get_status_all()
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

print("******************* SETTING UP THE STATUS AND CONTROLLING THE DEVICE_ID *******************\n\n")
COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_id(light_publisher1, {'switch_status': 'ON'})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_id(ac_publisher1, {'switch_status': 'ON'})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_id(light_publisher1, {'intensity': 'HIGH'})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_id(ac_publisher1, {'temperature': 30})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

print("******************* SETTING UP THE STATUS AND CONTROLLING BY THE DEVICE_TYPE *******************\n\n")


COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_device_type(
    'LIGHT', {'switch_status': 'ON', 'intensity': 'HIGH'})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_device_type(
    'LIGHT', {'switch_status': 'OFF'})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_device_type(
    'AC', {'switch_status': 'ON', 'temperature': 25})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

print("******************* SETTING UP THE STATUS AND CONTROLLING BY THE ROOM_TYPE *******************\n\n")

print("Controlling room type living_room\n")

COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_room_type(
    'living_room', {'temperature': 26})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

print("Controlling room type kitchen\n")
COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_room_type(
    'kitchen', {'intensity': 'MEDIUM'})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

print("Controlling room type bedroom\n")
COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_room_type(
    'bedroom', {'switch_status': 'ON', 'intensity': 'HIGH'})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

print("Controlling room type all\n")
COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_all(
    {'switch_status': 'ON', 'intensity': 'HIGH', 'temperature': 21})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

print("******************* SETTING UP THE STATUS AND CONTROLLING FOR INVALID REQUESTS*******************\n\n")

COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_id(light_publisher1, {'intensity': 'EXT'})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_id(ac_publisher1, {'temperature': 35})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_device_type('AC', {'temperature': 35})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.set_switch_status_room_type(
    'living_room', {'status': 'ON', 'intensity': 'MEDIUM', 'temperature': 35})
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")

print("******************* CURRENT STATUS BEFORE CLOSING THE PROGRAM *******************\n\n")
COMMAND_ID += 1
print(F"Command ID {COMMAND_ID} request is intiated.\n")
edge_server_1.get_status_all()
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")


edge_server_1.terminate()
