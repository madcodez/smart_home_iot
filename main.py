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
ac_publisher3 = AC_Device("ac_1", "bedroom")


# light_publisher = LightDevicePublisher("localhost", "my_client")
time.sleep(WAIT_TIME)


registered_devices = edge_server_1.get_registered_device_list()
device_ids = []
for device in registered_devices:
    device_ids.append(device['device_id'])
print('The Registered devices on Edge-Server:', device_ids)


print("******************* GETTING THE STATUS BY DEVICE_ID *******************\n\n")
for i in range(len(registered_devices)):

    COMMAND_ID = i + 1
    print(F"Command ID {COMMAND_ID} request is intiated.\n")

    edge_server_1.get_status_device_id(registered_devices[i]['device_id'])
    time.sleep(WAIT_TIME)
    print(f"Command ID {COMMAND_ID} is executed.\n")

# Creating the ac_device
# print("\nCreating the AC devices for their respective rooms. ")
# ac_device_1 = AC_Device("ac_1", "BR1")
# time.sleep(WAIT_TIME)
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
edge_server_1.get_status()
time.sleep(WAIT_TIME)
print(f"Command ID {COMMAND_ID} is executed.\n")
# print("\nSmart Home Simulation stopped.")

# edge_server_1.terminate()
