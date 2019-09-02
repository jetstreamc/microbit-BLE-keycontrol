import asyncio
import keyboard
import multiprocessing as mp
from enum import Enum
from bleak import BleakClient

address = "EE:37:52:D8:84:6B"

# UARTSERVICE_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
# UART_RX_CHARACTERISTIC_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UART_TX_CHARACTERISTIC_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

# mapping between pressed key and command to be send
press_keycmd_map = {
    'up': "F$",
    'down': "B$",
    'left': "L$",
    'right': "R$",
    '1': "1$",
    '2': "2$",
    '3': "3$",
    '4': "4$",
}

# mapping between released key and command to be send
release_keycmd_map = {
    'up': "S$",
    'down': "S$",
    'left': "S$",
    'right': "S$",
}

is_pressed = False
is_exited = False
q = mp.Queue()

async def send(client: BleakClient):
    if not q.empty():
        msg = q.get()
        print("send: {}".format(msg))
        await client.write_gatt_char(UART_TX_CHARACTERISTIC_UUID, bytearray(msg, 'ascii'))

def press_put_queue(event: keyboard.KeyboardEvent):
    global is_pressed
    if not is_pressed and event.name in press_keycmd_map:
        q.put(press_keycmd_map[event.name])
    is_pressed = True

def release_put_queue(event: keyboard.KeyboardEvent):
    global is_pressed
    if is_pressed and event.name in release_keycmd_map:
        q.put(release_keycmd_map[event.name])
    is_pressed = False

def set_exit():
    global is_exited
    is_exited = True

async def run(address, loop):

    print("Start connecting ...")
    
    async with BleakClient(address, loop=loop) as client:
        print("Connect!", end="\n\n")

        key_used = sorted(set(press_keycmd_map.keys()).union(release_keycmd_map.keys()))
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
