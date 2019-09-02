import asyncio
import keyboard
import multiprocessing as mp
from enum import Enum
from bleak import BleakClient

address = "EE:37:52:D8:84:6B"

# MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"
EVENT_SERVICE_UUID = "e95d93af-251d-470a-a062-fa1922dfa9a8"

CLIENT_REQUIREMENTS_CHARACTERISTIC_UUID = 'e95d23c4-251d-470a-a062-fa1922dfa9a8'
CLIENT_EVENT_CHARACTERISTIC_UUID        = 'e95d5404-251d-470a-a062-fa1922dfa9a8'

PRESS_VALUES = {
    'up': bytearray([80, 4, 1, 0]),
    'down': bytearray([80, 4, 3, 0]),
    'left': bytearray([80, 4, 5, 0]),
    'right': bytearray([80, 4, 7, 0]),
    '1': bytearray([80, 4, 9, 0]),
    '2': bytearray([80, 4, 11, 0]),
    '3': bytearray([80, 4, 13, 0]),
    '4': bytearray([80, 4, 15, 0]),
}

RELEASE_VALUES = {
    'up': bytearray([80, 4, 2, 0]),
    'down': bytearray([80, 4, 4, 0]),
    'left': bytearray([80, 4, 6, 0]),
    'right': bytearray([80, 4, 8, 0]),
    '1': bytearray([80, 4, 10, 0]),
    '2': bytearray([80, 4, 12, 0]),
    '3': bytearray([80, 4, 14, 0]),
    '4': bytearray([80, 4, 16, 0]),
}

is_pressed = False
is_exited = False
q = mp.Queue()

async def send(client: BleakClient):
    if not q.empty():
        msg = q.get()
        print("send: {}".format(msg))
        await client.write_gatt_char(CLIENT_EVENT_CHARACTERISTIC_UUID, msg)

def press_put_queue(event: keyboard.KeyboardEvent):
    global is_pressed
    if not is_pressed and event.name in PRESS_VALUES:
        q.put(PRESS_VALUES[event.name])
    is_pressed = True

def release_put_queue(event: keyboard.KeyboardEvent):
    global is_pressed
    if is_pressed and event.name in RELEASE_VALUES:
        q.put(RELEASE_VALUES[event.name])
    is_pressed = False

def set_exit():
    global is_exited
    is_exited = True

async def run(address, loop):

    print("Start connecting ...")

    async with BleakClient(address, loop=loop) as client:
        print("Connect!", end="\n\n")

        key_used = ['1', '2', '3', '4', 'up', 'down', 'left', 'right']
        for key in key_used:
            keyboard.on_press_key(key, press_put_queue, suppress=True)
            keyboard.on_release_key(key, release_put_queue, suppress=True)

        print("Key {} are now ready".format(key_used))

        keyboard.add_hotkey('q', set_exit, suppress=True)
        print("You can now control the robot via BLE UART. (press q to exit)", end="\n\n")

        while not is_exited:
            await send(client)
            
    print("Disconnected!")

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address, loop))
